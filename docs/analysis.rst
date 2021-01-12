Programming Model for Analysis
==============================

This page describes the programming model that SageMaker Debugger
provides for your analysis, and introduces you to the constructs of
Trial, Tensor and Rule.

Table of Contents
-----------------

-  `Rules <#Rules>`__

   -  `Built In Rules <#Built-In-Rules>`__
   -  `Writing a custom rule <#Writing-a-custom-rule>`__

      -  `Constructor <#Constructor>`__
      -  `Function to invoke at a given
         step <#Function-to-invoke-at-a-given-step>`__

   -  `Invoking a rule <#Invoking-a-rule>`__

      -  `invoke_rule <#invoke_rule>`__

-  `Exceptions <#Exceptions>`__
-  `Utils <#Utils>`__

   -  `Enable or disable refresh of tensors in a
      trial <#Enable-or-disable-refresh-of-tensors-in-a-trial>`__



Rules
-----

Rules are the medium by which SageMaker Debugger executes a certain
piece of code regularly on different steps of a training job. A rule is
assigned to a trial and can be invoked at each new step of the trial. It
can also access other trials for its evaluation. You can evaluate a rule
using tensors from the current step or any step before the current step.
Please ensure your logic respects these semantics, else you will get a
``TensorUnavailableForStep`` exception as the data would not yet be
available for future steps.

Built In Rules
~~~~~~~~~~~~~~

Please refer to the built-in rules that SageMaker provides
`here <https://github.com/awslabs/sagemaker-debugger/blob/master/docs/sagemaker.md#built-in-rules>`__.

Writing a custom rule
~~~~~~~~~~~~~~~~~~~~~

Writing a rule involves implementing the `Rule
interface <../smdebug/rules/rule.py>`__. Below, let us look at a
simplified version of a VanishingGradient rule.

Constructor
^^^^^^^^^^^

Creating a rule involves first inheriting from the base ``Rule`` class
provided by smdebug. For this example rule here, we do not need to look
at any other trials, so we set ``other_trials`` to None.

.. code:: python

   from smdebug.rules import Rule

   class VanishingGradientRule(Rule):
       def __init__(self, base_trial, threshold=0.0000001):
           super().__init__(base_trial, other_trials=None)
           self.threshold = float(threshold)

Please note that apart from ``base_trial`` and ``other_trials`` (if
required), we require all arguments of the rule constructor to take a
string as value. You can parse them to the type that you want from the
string. This means if you want to pass a list of strings, you might want
to pass them as a comma separated string. This restriction is being
enforced so as to let you create and invoke rules from json using
Sagemaker’s APIs.

Function to invoke at a given step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this function you can implement the core logic of what you want to do
with these tensors. It should return a boolean value ``True`` or
``False``, where ``True`` means the rule evaluation condition has been
met. When you invoke these rules through SageMaker, the rule evaluation
ends when the rule evaluation condition is met. SageMaker creates a
Cloudwatch event for every rule evaluation job, which can be used to
define actions that you might want to take based on the state of the
rule.

A simplified version of the actual invoke function for
``VanishingGradientRule`` is below:

.. code:: python

       def invoke_at_step(self, step):
           for tensorname in self.base_trial.tensors(collection='gradients'):
               tensor = self.base_trial.tensor(tensorname)
               abs_mean = tensor.reduction_value(step, 'mean', abs=True)
               if abs_mean < self.threshold:
                   return True
               else:
                   return False

That’s it, writing a rule is as simple as that.

Invoking a rule through SageMaker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After you’ve written your rule, you can ask SageMaker to evaluate the
rule against your training job by either using SageMaker Python SDK as

::

   estimator = Estimator(
       ...
       rules = Rules.custom(
           name='VGRule',
           image_uri='864354269164.dkr.ecr.us-east-1.amazonaws.com/sagemaker-debugger-rule-evaluator:latest',
           instance_type='ml.t3.medium', # instance type to run the rule evaluation on
           source='rules/vanishing_gradient_rule.py', # path to the rule source file
           rule_to_invoke='VanishingGradientRule', # name of the class to invoke in the rule source file
           volume_size_in_gb=30, # EBS volume size required to be attached to the rule evaluation instance
           collections_to_save=[CollectionConfig("gradients")], # collections to be analyzed by the rule
           rule_parameters={
               "threshold": "20.0" # this will be used to initialize 'threshold' param in your rule constructor
           }
   )

If you’re using the SageMaker API directly to evaluate the rule, then
you can specify the rule configuration
```DebugRuleConfigurations`` <https://docs.aws.amazon.com/sagemaker/latest/dg/API_DebugRuleConfiguration.html>`__
in the CreateTrainingJob API request as:

::

   "DebugRuleConfigurations": [
       {
           "RuleConfigurationName": "VGRule",
           "InstanceType": "ml.t3.medium",
           "VolumeSizeInGB": 30,
           "RuleEvaluatorImage": "864354269164.dkr.ecr.us-east-1.amazonaws.com/sagemaker-debugger-rule-evaluator:latest",
           "RuleParameters": {
               "source_s3_uri": "s3://path/to/vanishing_gradient_rule.py",
               "rule_to_invoke": "VanishingGradient",
               "threshold": "20.0"
           }
       }
   ]

Invoking a rule outside of SageMaker through ``invoke_rule``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might want to invoke the rule locally during development. We provide
a function to invoke rules easily. Refer
`smdebug/rules/rule_invoker.py <../smdebug/rules/rule_invoker.py>`__.
The invoke function has the following syntax. It takes a instance of a
Rule and invokes it for a series of steps one after the other.

.. code:: python

   from smdebug.rules import invoke_rule
   from smdebug.trials import create_trial

   trial = create_trial('s3://smdebug-dev-test/mnist-job/')
   rule_obj = VanishingGradientRule(trial, threshold=0.0001)
   invoke_rule(rule_obj, start_step=0, end_step=None)

.. _arguments-19:

Arguments
'''''''''

-  ``rule_obj (Rule)`` An instance of a subclass of
   ``smdebug.rules.Rule`` that you want to invoke.
-  ``start_step (int)`` Global step number to start invoking the rule
   from. Note that this refers to a global step. This defaults to 0.
-  ``end_step (int or  None)``: Global step number to end the invocation
   of rule before. To clarify, ``end_step`` is an exclusive bound. The
   rule is invoked at ``end_step``. This defaults to ``None`` which
   means run till the end of the job.
-  ``raise_eval_cond (bool)`` This parameter controls whether to raise
   the exception ``RuleEvaluationConditionMet`` when raised by the rule,
   or to catch it and log the message and move to the next step.
   Defaults to ``False``, which implies that the it catches the
   exception, logs that the evaluation condition was met for a step and
   moves on to evaluate the next step.

Exceptions
----------

smdebug is designed to be aware that tensors required to evaluate a rule
may not be available at every step. Hence, it raises a few exceptions
which allow us to control what happens when a tensor is missing. These
are available in the ``smdebug.exceptions`` module. You can import them
as follows:

.. code:: python

   from smdebug.exceptions import *

Here are the exceptions (along with others) and their meaning:

-  ``TensorUnavailableForStep`` : This means that the tensor requested
   is not available for the step. It may have been or will be saved for
   a different step number. You can check which steps tensor is saved
   for by ``trial.tensor('tname').steps()``
   `api <https://github.com/awslabs/sagemaker-debugger/blob/master/docs/analysis.md#steps-1>`__.
   Note that this exception implies that the requested tensor will never
   become available for this step in the future.

-  ``TensorUnavailable`` : This means that this tensor has not been
   saved from the training job. Note that if you have a ``SaveConfig``
   which saves a certain tensor only after the time you queried for the
   tensor, you might get a ``TensorUnavailable`` exception even if the
   tensor may become available later for some step.

-  ``StepUnavailable``: This means that the step was not saved from the
   training job. No tensor will be available for this step.

-  ``StepNotYetAvailable``: This means that the step has not yet been
   seen from the training job. It may be available in the future if the
   training is still going on. We automatically load new data as and
   when it becomes available. This step may either become available in
   the future, or the exception might change to ``StepUnavailable``.

-  ``NoMoreData`` : This will be raised when the training ends. Once you
   see this, you will know that there will be no more steps and no more
   tensors saved.

-  ``RuleEvaluationConditionMet``: This is raised when the rule
   invocation returns ``True`` for some step.

-  ``MissingCollectionFiles``: This is raised when no data was saved by
   the training job. Check that the ``Hook`` was configured correctly
   before starting the training job.

Utils
-----

Enable or disable refresh of tensors in a trial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default smdebug refreshes tensors each time you try to query the
tensor. It looks for whether this tensor is saved for new steps and if
so fetches them. If you know the saved data will not change (stopped the
machine learning job), or are not interested in the latest data, you can
stop the refreshing of tensors as follows:

``no_refresh`` takes a trial or a list of trials, which should not be
refreshed. Anything executed inside the with ``no_refresh`` block will
not be refreshed.

.. code:: python

   from smdebug.analysis.utils import no_refresh
   with no_refresh(trials):
       pass

Similarly if you want to refresh tensors only within a block, you can
do:

.. code:: python

   from smdebug.analysis.utils import refresh
   with refresh(trials):
       pass

During rule invocation smdebug waits till the current step is available
and then turns off refresh to ensure that you do not get different
results for methods like ``trial.tensor(name).steps()`` and run into
subtle issues.
