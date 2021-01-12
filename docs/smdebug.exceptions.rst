smdebug.exceptions module
-------------------------

.. automodule:: smdebug.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

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
