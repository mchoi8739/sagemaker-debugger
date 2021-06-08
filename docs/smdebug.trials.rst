smdebug.trials package
======================

.. autoclass:: smdebug.trials.create_trial

Trial is an object which lets you query for tensors for a given training
job, specified by the path where smdebug’s artifacts are saved. Trial is
capable of loading new tensors as and when they become available at the
given path, allowing you to do both offline as well as realtime
analysis.

Path of trial
~~~~~~~~~~~~~

SageMaker training job
^^^^^^^^^^^^^^^^^^^^^^

When running a SageMaker job this path is on S3. SageMaker saves data
from your training job locally on the training instance first and
uploads them to an S3 location in your account. When you start a
SageMaker training job with the python SDK, you can control this path
using the parameter ``s3_output_path`` in the ``DebuggerHookConfig``
object. This is an optional parameter, if you do not pass this the
python SDK will populate a default location for you. If you do pass
this, make sure the bucket is in the same region as where the training
job is running. If you’re not using the python SDK, set this path for
the parameter ``S3OutputPath`` in the ``DebugHookConfig`` section of
``CreateTrainingJob`` API. SageMaker takes this path and appends
training_job_name and “debug-output” to it to ensure we have a unique
path for each training job.

Non SageMaker training jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are not running a SageMaker training job, this is the path you
pass as ``out_dir`` when you create a smdebug
```Hook`` <api.md#hook>`__. Just like when creating the hook, you can
pass either a local path or an S3 path (as ``s3://bucket/prefix``).

Creating a trial object
~~~~~~~~~~~~~~~~~~~~~~~

There are two types of trials you can create: LocalTrial or S3Trial
depending on the path. We provide a wrapper method to create the
appropriate trial.

The parameters you have to provide are:

- ``path`` (str): A local path or an S3 path of the form ``s3://bucket/prefix``. You should see
  directories such as ``collections``, ``events`` and ``index`` at this
  path once the training job starts.

- ``name`` (str): A name for a trial.
  It is to help you manage different trials. This is an optional
  parameter, which defaults to the basename of the path if not passed.
  Please make sure to give it a unique name to prevent confusion.

Creating S3 trial
^^^^^^^^^^^^^^^^^

.. code:: python

 from smdebug.trials import create_trial
 trial = create_trial(
   path='s3://smdebug-testing-bucket/outputs/resnet',
   name='resnet_training_run'
 )

Creating local trial
^^^^^^^^^^^^^^^^^^^^

.. code:: python

 from smdebug.trials import create_trial
 trial = create_trial(
   path='/home/ubuntu/smdebug_outputs/resnet',
   name='resnet_training_run'
 )

Restricting analysis to a range of steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can optionally pass ``range_steps`` to restrict your analysis to a
certain range of steps. Note that if you do so, Trial will not load data
from other steps.

**Examples**

- ``range_steps=(100, None)``: This will load all steps after 100

- ``range_steps=(None, 100)``: This will load all steps before 100

- ``range_steps=(100, 200)`` : This will load steps between 100 and 200

- ``range_steps=None``: This will load all steps

.. code:: python

 from smdebug.trials import create_trial
 trial = create_trial(
   path='s3://smdebug-testing-bucket/outputs/resnet',
   name='resnet_training',
   range_steps=(100, 200)
 )

smdebug.trials.trial module
---------------------------

.. autoclass:: smdebug.trials.trial
   :members:
   :undoc-members:
   :show-inheritance:



Trial API
~~~~~~~~~

Here’s a list of methods that the Trial API provides which helps you
load data for analysis. Please click on the method to see all the
parameters it takes and a detailed description. If you are not familiar
with smdebug constructs, you might want to review :doc:`SMDebug APIs <api>`
before going through this page.

+-----------------------------------+-----------------------------------+
| Method                            | Description                       |
+===================================+===================================+
| `trial.tensor_names()             | See names of all tensors          |
| <#tensor_names>`__                | available                         |
+-----------------------------------+-----------------------------------+
| `trial.tensor(name) <#tensor>`__  | Retrieve smdebug Tensor object    |
+-----------------------------------+-----------------------------------+
| `trial.has_tensor(name)           | Query for whether tensor was      |
| <#has_tensor>`__                  | saved                             |
+-----------------------------------+-----------------------------------+
| `trial.steps() <#steps>`__        | Query steps for which data was    |
|                                   | saved                             |
+-----------------------------------+-----------------------------------+
| `trial.modes() <#modes>`__        | Query modes for which data was    |
|                                   | saved                             |
+-----------------------------------+-----------------------------------+
| `trial.mode(step) <#mode>`__      | Query the mode for a given global |
|                                   | step                              |
+-----------------------------------+-----------------------------------+
| `trial.global_step(mode,          | Query global step for a given     |
| step) <#global_step>`__           | step and mode                     |
+-----------------------------------+-----------------------------------+
| `trial.mode_step(step)            | Query the mode step for a given   |
| <#mode_step>`__                   | global step                       |
+-----------------------------------+-----------------------------------+
| `trial.workers() <#workers>`__    | Query list of workers from the    |
|                                   | data saved                        |
+-----------------------------------+-----------------------------------+
| `trial.collections()              | Query list of collections saved   |
| <#collections>`__                 | from the training job             |
+-----------------------------------+-----------------------------------+
| `trial.collection(name)           | Retrieve a single collection      |
| <#collection>`__                  | saved from the training job       |
+-----------------------------------+-----------------------------------+
| `trial.wait_for_steps(steps)      | Wait till the requested steps are |
| <#wait_for_steps>`__              | available                         |
+-----------------------------------+-----------------------------------+
| `trial.has_passed_step(step)      | Query whether the requested step  |
| <#has_passed_step>`__             | is available                      |
+-----------------------------------+-----------------------------------+

tensor_names
^^^^^^^^^^^^

Retrieves names of tensors saved

.. code:: python

  trial.tensor_names(
    step= None,
    mode=modes.GLOBAL,
    regex=None,
    collection=None
  )

Arguments
'''''''''

All arguments to this method are optional. You are not required to pass
any of these arguments as keyword arguments.

-  ``step (int)`` If you want to retrieve the list of tensors saved at a
  particular step, pass the step number as an integer. This step number
  will be treated as step number corresponding to the mode passed
  below. By default it is treated as global step.

-  ``mode (smdebug.modes enum value)`` If you want to retrieve the list
  of tensors saved for a particular mode, pass the mode here as
  ``smd.modes.TRAIN``, ``smd.modes.EVAL``, ``smd.modes.PREDICT``, or
  ``smd.modes.GLOBAL``.

-  ``regex (str or list[str])`` You can filter tensors matching regex
  expressions by passing a regex expressions as a string or list of
  strings. You can only pass one of ``regex`` or ``collection``
  parameters.

-  ``collection (Collection or str)`` You can filter tensors belonging
  to a collection by either passing a collection object or the name of
  collection as a string. You can only pass one of ``regex`` or
  ``collection`` parameters.

Returns
'''''''

``list[str]``: List of strings representing names of tensors matching
  the given arguments. Arguments are processed as follows: get the list of
  tensor names for given step and mode, saved for given step matching all
  the given arguments, i.e. intersection of tensors matching each of the
  parameters.

Examples
''''''''

-  ``trial.tensor_names()`` Returns all tensors saved for any step or
  mode.
-  ``trial.tensor_names(step=10, mode=modes.TRAIN)`` Returns tensors
  saved for training step 10
-  ``trial.tensor_names(regex='relu')`` Returns all tensors matching the
  regex pattern ``relu`` saved for any step or mode.
-  ``trial.tensor_names(collection='gradients')`` Returns tensors from
  collection “gradients”
-  ``trial.tensor_names(step=10, mode=modes.TRAIN, regex='softmax')``
  Returns tensor saved for 10th training step which matches the regex
  ``softmax``

tensor
^^^^^^

Retrieve the ``smdebug.core.tensor.Tensor`` object by the given name
``tname``. You can review all the methods that this Tensor object
provides `here <#Tensor-1>`__.

.. code:: python

  trial.tensor(tname)

.. _arguments-1:

Arguments
'''''''''

-  ``tname (str)`` Takes the name of tensor

.. _returns-1:

Returns
'''''''

``smdebug.core.tensor.Tensor`` object which has `this API <#Tensor-1>`__

has_tensor
^^^^^^^^^^

Query whether the trial has a tensor by the given name

.. code:: python

trial.has_tensor(tname)

.. _arguments-2:

Arguments
'''''''''

-  ``tname (str)`` Takes the name of tensor

.. _returns-2:

Returns
'''''''

``bool``: ``True`` if the tensor is seen by the trial so far, else
``False``.

steps
^^^^^

Retrieve a list of steps seen by the trial

.. code:: python

trial.steps(mode=None)

.. _arguments-3:

Arguments
'''''''''

-  ``mode (smdebug.modes enum value)`` Passing a mode here allows you
want to retrieve the list of steps seen by a trial for that mode If
this is not passed, returns steps for all modes.

.. _returns-3:

Returns
'''''''

``list[int]`` List of integers representing step numbers. If a mode was
passed, this returns steps within that mode, i.e. mode steps. Each of
these mode steps has a global step number associated with it. The global
step represents the sequence of steps across all modes executed by the
job.

modes
^^^^^

Retrieve a list of modes seen by the trial

.. code:: python

  trial.modes()

.. _returns-4:

Returns
'''''''

``list[smdebug.modes enum value]`` List of modes for which data was
saved from the training job across all steps seen.

mode
^^^^

Given a global step number you can identify the mode for that step using
this method.

.. code:: python

  trial.mode(global_step=100)

.. _arguments-4:

Arguments
'''''''''

-  ``global_step (int)`` Takes the global step as an integer

.. _returns-5:

Returns
'''''''

``smdebug.modes enum value`` of the given global step

mode_step
^^^^^^^^^

Given a global step number you can identify the ``mode_step`` for that
step using this method.

.. code:: python

  trial.mode_step(global_step=100)

.. _arguments-5:

Arguments
'''''''''

-  ``global_step (int)`` Takes the global step as an integer

.. _returns-6:

Returns
'''''''

``int``: An integer representing ``mode_step`` of the given global step.
Typically used in conjunction with ``mode`` method.

global_step
^^^^^^^^^^^

Given a mode and a mode_step number you can retrieve its global step
using this method.

.. code:: python

  trial.global_step(mode=modes.GLOBAL, mode_step=100)

.. _arguments-6:

Arguments
'''''''''

-  ``mode (smdebug.modes enum value)`` Takes the mode as enum value
-  ``mode_step (int)`` Takes the mode step as an integer

.. _returns-7:

Returns
'''''''

``int`` An integer representing ``global_step`` of the given mode and
mode_step.

workers
^^^^^^^

Query for all the worker processes from which data was saved by smdebug
during multi worker training.

.. code:: python

  trial.workers()

.. _returns-8:

Returns
'''''''

``list[str]`` A sorted list of names of worker processes from which data
was saved. If using TensorFlow Mirrored Strategy for multi worker
training, these represent names of different devices in the process. For
Horovod, torch.distributed and similar distributed training approaches,
these represent names of the form ``worker_0`` where 0 is the rank of
the process.

collections
^^^^^^^^^^^

List the collections from the trial. Note that tensors part of these
collections may not necessarily have been saved from the training job.
Whether a collection was saved or not depends on the configuration of
the Hook during training.

.. code:: python

  trial.collections()

.. _returns-9:

Returns
'''''''

``dict[str -> Collection]`` A dictionary indexed by the name of the
collection, with the Collection object as the value. Please refer
`Collection API <api.md#Collection>`__ for more details.

collection
^^^^^^^^^^

Get a specific collection from the trial. Note that tensors which are
part of this collection may not necessarily have been saved from the
training job. Whether this collection was saved or not depends on the
configuration of the Hook during training.

.. code:: python

  trial.collection(coll_name)

.. _arguments-7:

Arguments
'''''''''

-  ``coll_name (str)`` Name of the collection

.. _returns-10:

Returns
'''''''

``Collection`` The requested Collection object. Please refer `Collection
API <api.md#Collection>`__ for more details.

wait_for_steps
^^^^^^^^^^^^^^

This method allows you to wait for steps before proceeding. You might
want to use this method if you want to wait for smdebug to see the
required steps so you can then query and analyze the tensors saved by
that step. This method blocks till all data from the steps are seen by
smdebug.

.. code:: python

  trial.wait_for_steps(required_steps, mode=modes.GLOBAL)

.. _arguments-8:

Arguments
'''''''''

-  ``required_steps (list[int])`` Step numbers to wait for
-  ``mode (smdebug.modes enum value)`` The mode to which given step
numbers correspond to. This defaults to modes.GLOBAL.

.. _returns-11:

Returns
'''''''

None, but it only returns after we know definitely whether we have seen
the steps.

Exceptions raised
'''''''''''''''''

``StepUnavailable`` and ``NoMoreData``. See `Exceptions <#exceptions>`__
section for more details.

has_passed_step
^^^^^^^^^^^^^^^

.. code:: python

  trial.has_passed_step(step, mode=modes.GLOBAL)

.. _arguments-9:

Arguments
'''''''''

-  ``step (int)`` The step number to check if the trial has passed it
-  ``mode (smdebug.modes enum value)`` The mode to which given step
  number corresponds to. This defaults to modes.GLOBAL.

.. _returns-12:

Returns
'''''''

``smdebug.core.tensor.StepState enum value`` which can take one of three
values ``UNAVAILABLE``, ``AVAILABLE`` and ``NOT_YET_AVAILABLE``.

TODO@Nihal describe these in detail

.. _tensor-1:

Tensor
------

An smdebug ``Tensor`` object can be retrieved through the
``trial.tensor(name)`` API. It is uniquely identified by the string
representing name. It provides the following methods.

+-------------------------------+---------------------------------------+
| Method                        | Description                           |
+===============================+=======================================+
| `steps() <#steps-1>`__        | Query steps for which tensor was      |
|                               | saved                                 |
+-------------------------------+---------------------------------------+
| `value(step) <#value>`__      | Get the value of the tensor at a      |
|                               | given step as a numpy array           |
+-------------------------------+---------------------------------------+
| `reduction_value(step)        | Get the reduction value of the chosen |
| <#reduction_value>`__         | tensor at a particular step           |
+-------------------------------+---------------------------------------+
| `reduction_values             | Get all reduction values saved for    |
| (step) <#reduction_values>`__ | the chosen tensor at a particular     |
|                               | step                                  |
+-------------------------------+---------------------------------------+
| `values(mode) <#values>`__    | Get the values of the tensor for all  |
|                               | steps of a given mode                 |
+-------------------------------+---------------------------------------+
| `                             | Get all the workers for which this    |
| workers(step) <#workers-1>`__ | tensor was saved at a given step      |
+-------------------------------+---------------------------------------+
| `prev_steps(step,             | Get the last n step numbers of a      |
| n) <#prev_steps>`__           | given mode from a given step          |
+-------------------------------+---------------------------------------+

Tensor API
~~~~~~~~~~

.. _steps-1:

steps
^^^^^

Query for the steps at which the given tensor was saved

.. code:: python

  trial.tensor(name).steps(mode=ModeKeys.GLOBAL, show_incomplete_steps=False)

.. _arguments-10:

Arguments
'''''''''

-  ``mode (smdebug.modes enum value)`` The mode whose steps to return
  for the given tensor. Defaults to ``modes.GLOBAL``
-  ``show_incomplete_steps (bool)`` This parameter is relevant only for
  distributed training. By default this method only returns the steps
  which have been received from all workers. But if this parameter is
  set to True, this method will return steps received from at least one
  worker.

.. _returns-13:

Returns
'''''''

``list[int]`` A list of steps at which the given tensor was saved

value
^^^^^

Get the value of the tensor at a given step as a numpy array

.. code:: python

  trial.tensor(name).value(step_num, mode=ModeKeys.GLOBAL, worker=None)

.. _arguments-11:

Arguments
'''''''''

-  ``step_num (int)`` The step number whose value is to be returned for
  the mode passed through the next parameter.
-  ``mode (smdebug.modes enum value)`` The mode applicable for the step
  number passed above. Defaults to ``modes.GLOBAL``
-  ``worker (str)`` This parameter is only applicable for distributed
  training. You can retrieve the value of the tensor from a specific
  worker by passing the worker name. You can query all the workers seen
  by the trial with the ``trial.workers()`` method. You might also be
  interested in querying the workers which saved a value for the tensor
  at a specific step, this is possible with the method:
  ``trial.tensor(name).workers(step, mode)``

.. _returns-14:

Returns
'''''''

``numpy.ndarray`` The value of tensor at the given step and worker (if
the training job saved data from multiple workers)

reduction_value
^^^^^^^^^^^^^^^

Get the reduction value of the chosen tensor at a particular step. A
reduction value is a tensor reduced to a single value through reduction
or aggregation operations. The different reductions you can query for
are the same as what are allowed in
`ReductionConfig <api.md#reductionconfig>`__ when saving tensors. This
API thus allows you to access the reduction you might have saved instead
of the full tensor. If you had saved the full tensor, it will calculate
the requested reduction at the time of this call.

Reduction names allowed are ``min``, ``max``, ``mean``, ``prod``,
``std``, ``sum``, ``variance`` and ``l1``, ``l2`` representing the
norms.

Each of these can be retrieved for the absolute value of the tensor or
the original tensor. Above was an example to get the mean of the
absolute value of the tensor. ``abs`` can be set to ``False`` if you
want to see the ``mean`` of the actual tensor.

If you had saved the tensor without any reduction, then you can retrieve
the actual tensor as a numpy array and compute any reduction you might
be interested in. In such a case you do not need this method.

.. code:: python

  trial.tensor(name).reduction_value(
    step_num,
    reduction_name,
    mode=modes.GLOBAL,
    worker=None,
    abs=False
  )

.. _arguments-12:

Arguments
'''''''''

-  ``step_num (int)`` The step number whose value is to be returned for
  the mode passed through the next parameter.
-  ``reduction_name (str)`` The name of the reduction to query for. This
  can be one of ``min``, ``max``, ``mean``, ``std``, ``variance``,
  ``sum``, ``prod`` and the norms ``l1``, ``l2``.
-  ``mode (smdebug.modes enum value)`` The mode applicable for the step
  number passed above. Defaults to ``modes.GLOBAL``
-  ``worker (str)`` This parameter is only applicable for distributed
  training. You can retrieve the value of the tensor from a specific
  worker by passing the worker name. You can query all the workers seen
  by the trial with the ``trial.workers()`` method. You might also be
  interested in querying the workers which saved a value for the tensor
  at a specific step, this is possible with the method:
  ``trial.tensor(name).workers(step, mode)``
-  ``abs (bool)`` If abs is True, this method tries to return the
  reduction passed through ``reduction_name`` after taking the absolute
  value of the tensor. It defaults to ``False``.

.. _returns-15:

Returns
'''''''

``numpy.ndarray`` The reduction value of tensor at the given step and
worker (if the training job saved data from multiple workers) as a 1x1
numpy array. If this reduction was saved for the tensor during training
as part of specification through reduction config, it will be loaded and
returned. If the given reduction was not saved then, but the full tensor
was saved, the reduction will be computed on the fly and returned. If
both the chosen reduction and full tensor are not available, this method
raises ``TensorUnavailableForStep`` exception.

shape
^^^^^

Get the shape of the chosen tensor at a particular step.

.. code:: python

  trial.tensor(name).shape(step_num, mode=modes.GLOBAL, worker=None)

.. _arguments-13:

Arguments
'''''''''

-  ``step_num (int)`` The step number whose value is to be returned for
  the mode passed through the next parameter.
-  ``mode (smdebug.modes enum value)`` The mode applicable for the step
  number passed above. Defaults to ``modes.GLOBAL``
-  ``worker (str)`` This parameter is only applicable for distributed
  training. You can retrieve the value of the tensor from a specific
  worker by passing the worker name. You can query all the workers seen
  by the trial with the ``trial.workers()`` method. You might also be
  interested in querying the workers which saved a value for the tensor
  at a specific step, this is possible with the method:
  ``trial.tensor(name).workers(step, mode)``

.. _returns-16:

Returns
'''''''

- ``tuple(int)`` If only the shape of this tensor was saved through.
- ``save_shape`` configuration in ReductionConfig, it will be returned. If
  the full tensor was saved, then shape will be computed and returned
  today. If both the shape and full tensor are not available, this method
  raises ``TensorUnavailableForStep`` exception.

values
^^^^^^

Get the values of the tensor for all steps of a given mode.

.. code:: python

  trial.tensor(name).values(mode=modes.GLOBAL, worker=None)

.. _arguments-14:

Arguments
'''''''''

-  ``mode (smdebug.modes enum value)`` The mode applicable for the step
  number passed above. Defaults to ``modes.GLOBAL``
-  ``worker (str)`` This parameter is only applicable for distributed
  training. You can retrieve the value of the tensor from a specific
  worker by passing the worker name. You can query all the workers seen
  by the trial with the ``trial.workers()`` method. You might also be
  interested in querying the workers which saved a value for the tensor
  at a specific step, this is possible with the method:
  ``trial.tensor(name).workers(step, mode)``

.. _returns-17:

Returns
'''''''

``dict[int -> numpy.ndarray]`` A dictionary with step numbers as keys
and numpy arrays representing the value of the tensor as values.

reduction_values
^^^^^^^^^^^^^^^^

Get all reduction values saved for the chosen tensor at a particular
step. A reduction value is a tensor reduced to a single value through
reduction or aggregation operations. Please go through the description
of the method ``reduction_value`` for more details.

.. code:: python

  trial.tensor(name).reduction_values(step_num, mode=modes.GLOBAL, worker=None)

.. _arguments-15:

Arguments
'''''''''

-  ``step_num (int)`` The step number whose value is to be returned for
  the mode passed through the next parameter.
-  ``mode (smdebug.modes enum value)`` The mode applicable for the step
  number passed above. Defaults to ``modes.GLOBAL``
-  ``worker (str)`` This parameter is only applicable for distributed
  training. You can retrieve the value of the tensor from a specific
  worker by passing the worker name. You can query all the workers seen
  by the trial with the ``trial.workers()`` method. You might also be
  interested in querying the workers which saved a value for the tensor
  at a specific step, this is possible with the method:
  ``trial.tensor(name).workers(step, mode)``

.. _returns-18:

Returns
'''''''

``dict[(str, bool) -> numpy.ndarray]`` A dictionary with keys being
tuples of the form ``(reduction_name, abs)`` to a 1x1 numpy ndarray
value. ``abs`` here is a boolean that denotes whether the reduction was
performed on the absolute value of the tensor or not. Note that this
method only returns the reductions which were saved from the training
job. It does not compute all known reductions and return them if only
the raw tensor was saved.

shapes
^^^^^^

Get the shapes of the tensor for all steps of a given mode.

.. code:: python

  trial.tensor(name).shapes(mode=modes.GLOBAL, worker=None)

.. _arguments-16:

Arguments
'''''''''

-  ``mode (smdebug.modes enum value)`` The mode applicable for the step
  number passed above. Defaults to ``modes.GLOBAL``
-  ``worker (str)`` This parameter is only applicable for distributed
  training. You can retrieve the value of the tensor from a specific
  worker by passing the worker name. You can query all the workers seen
  by the trial with the ``trial.workers()`` method. You might also be
  interested in querying the workers which saved a value for the tensor
  at a specific step, this is possible with the method:
  ``trial.tensor(name).workers(step, mode)``

.. _returns-19:

Returns
'''''''

``dict[int -> tuple(int)]`` A dictionary with step numbers as keys and
tuples of ints representing the shapes of the tensor as values.

.. _workers-1:

workers
^^^^^^^

Get all the workers for which this tensor was saved at a given step

.. code:: python

  trial.tensor(name).workers(step_num, mode=modes.GLOBAL)

.. _arguments-17:

Arguments
'''''''''

-  ``step_num (int)`` The step number whose value is to be returned for
  the mode passed through the next parameter.
-  ``mode (smdebug.modes enum value)`` The mode applicable for the step
  number passed above. Defaults to ``modes.GLOBAL``

.. _returns-20:

Returns
'''''''

``list[str]`` A list of worker names for which the tensor was saved at
the given step.

prev_steps
^^^^^^^^^^

Get the last n step numbers of a given mode from a given step.

.. code:: python

  trial.tensor(name).prev_steps(step, n, mode=modes.GLOBAL)

.. _arguments-18:

Arguments
'''''''''

- ``step (int)`` The step number whose value is to be returned for the
  mode passed.
- ``n (int)`` Number of previous steps to return
- ``mode (smdebug.modes enum value)`` The mode applicable for the step
number passed above. Defaults to ``modes.GLOBAL``

.. _returns-21:

Returns
'''''''

``list[int]`` A list of size at most n representing the previous steps
for the given step and mode. Note that this list can be of size less
than n if there were only less than n steps saved before the given step
in this trial.
