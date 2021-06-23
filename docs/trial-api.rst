Trial API
---------

The following table shows a list of methods that an SMDebug trial object provides to help you
load data for output tensor analysis. Click on the method to see all the
parameters it requires and descriptions. If you are not familiar
with smdebug constructs, you might want to review :doc:`SMDebug APIs <api>`
before going through this page.

.. autoclass:: smdebug.trials.trial.Trial
  :members:
  :inherited-members:

.. autoclass::  smdebug.trials.create_trial
  :members:
  :undoc-members:
  :show-inheritance:
  :inherited-members:

.. note::
  To use the following trial methods, you must create a ``trial`` object as guided
  in the `SMDebug Trial <smdebug.trials>`__ page.

+-----------------------------------------------------------+-----------------------------------+
| Method                                                    | Description                       |
+===========================================================+===================================+
| `trial.tensor_names() <#trial.tensor_names>`__            | See names of all tensors          |
|                                                           | available                         |
+-----------------------------------------------------------+-----------------------------------+
| `trial.tensor(tname) <#trial.tensor>`__                   | Retrieve smdebug Tensor object    |
+-----------------------------------------------------------+-----------------------------------+
| `trial.has_tensor(tname) <#trial.has_tensor>`__           | Query for whether tensor was      |
|                                                           | saved                             |
+-----------------------------------------------------------+-----------------------------------+
| `trial.steps() <#trial.steps>`__                          | Query steps for which data was    |
|                                                           | saved                             |
+-----------------------------------------------------------+-----------------------------------+
| `trial.modes() <#trial.modes>`__                          | Query modes for which data was    |
|                                                           | saved                             |
+-----------------------------------------------------------+-----------------------------------+
| `trial.mode(step) <#trial.mode>`__                        | Query the mode for a given global |
|                                                           | step                              |
+-----------------------------------------------------------+-----------------------------------+
| `trial.global_step(mode,step) <#trial.global_step>`__     | Query global step for a given     |
|                                                           | step and mode                     |
+-----------------------------------------------------------+-----------------------------------+
| `trial.mode_step(step) <#trial.mode_step>`__              | Query the mode step for a given   |
|                                                           | global step                       |
+-----------------------------------------------------------+-----------------------------------+
| `trial.workers() <#trial.workers>`__                      | Query list of workers from the    |
|                                                           | data saved                        |
+-----------------------------------------------------------+-----------------------------------+
| `trial.collections() <#trial.collections>`__              | Query list of collections saved   |
|                                                           | from the training job             |
+-----------------------------------------------------------+-----------------------------------+
| `trial.collection(name) <#trial.collection>`__            | Retrieve a single collection      |
|                                                           | saved from the training job       |
+-----------------------------------------------------------+-----------------------------------+
| `trial.wait_for_steps(steps) <#trial.wait_for_steps>`__   | Wait till the requested steps are |
|                                                           | available                         |
+-----------------------------------------------------------+-----------------------------------+
| `trial.has_passed_step(step) <#trial.has_passed_step>`__  | Query whether the requested step  |
|                                                           | is available                      |
+-----------------------------------------------------------+-----------------------------------+


.. method:: trial.tensor_names(step= None, mode=modes.GLOBAL, regex=None, collection=None)

  Retrieves names of tensors saved

  **Parameters:**

    All arguments to this method are optional. You are not required to pass
    any of these arguments as keyword arguments.

    - ``step (int)`` - If you want to retrieve the list of tensors saved at a
      particular step, pass the step number as an integer. This step number
      will be treated as step number corresponding to the mode passed
      below. By default it is treated as global step.

    - ``mode (smdebug.modes enum value)`` - If you want to retrieve the list
      of tensors saved for a particular mode, pass the mode here as
      ``smd.modes.TRAIN``, ``smd.modes.EVAL``, ``smd.modes.PREDICT``, or
      ``smd.modes.GLOBAL``.

    - ``regex (str or list[str])`` - You can filter tensors matching regex
      expressions by passing a regex expressions as a string or list of
      strings. You can only pass one of ``regex`` or ``collection``
      parameters.

    - ``collection (Collection or str)`` - You can filter tensors belonging
      to a collection by either passing a collection object or the name of
      collection as a string. You can only pass one of ``regex`` or
      ``collection`` parameters.

  **Returns:**

    ``list[str]`` - List of strings representing names of tensors matching
    the given arguments. Arguments are processed as follows: get the list of
    tensor names for given step and mode, saved for given step matching all
    the given arguments, i.e. intersection of tensors matching each of the
    parameters.

  **Examples:**

    - ``trial.tensor_names()`` - Returns all tensors saved for any step or
      mode.
    - ``trial.tensor_names(step=10, mode=modes.TRAIN)`` - Returns tensors
      saved for training step 10
    - ``trial.tensor_names(regex='relu')`` - Returns all tensors matching the
      regex pattern ``relu`` saved for any step or mode.
    - ``trial.tensor_names(collection='gradients')`` - Returns tensors from
      collection “gradients”
    - ``trial.tensor_names(step=10, mode=modes.TRAIN, regex='softmax')`` -
      Returns tensor saved for 10th training step which matches the regex
      ``softmax``

.. method:: trial.tensor(tname)

  Retrieve the ``smdebug.core.tensor.Tensor`` object by the given name
  ``tname``. You can review all the methods that this Tensor object
  provides `here <#Tensor-1>`__.

  **Parameters:**

    - ``tname (str)`` - Takes the name of tensor

  **Returns:**

    ``smdebug.core.tensor.Tensor`` object which has `this API <#Tensor-1>`__

.. method:: trial.has_tensor(tname)

  Query whether the trial has a tensor by the given name

  **Parameters:**

    - ``tname (str)`` Takes the name of tensor

  **Returns:**

    ``bool``: ``True`` if the tensor is seen by the trial so far, else
    ``False``.

.. method:: trial.steps(mode=None)

  Retrieve a list of steps seen by the trial

  **Parameters:**

    - ``mode (smdebug.modes enum value)`` Passing a mode here allows you
      want to retrieve the list of steps seen by a trial for that mode If
      this is not passed, returns steps for all modes.

  **Returns:**

    ``list[int]`` List of integers representing step numbers. If a mode was
    passed, this returns steps within that mode, i.e. mode steps. Each of
    these mode steps has a global step number associated with it. The global
    step represents the sequence of steps across all modes executed by the
    job.

.. method:: trial.modes()

  Retrieve a list of modes seen by the trial

  **Returns:**

    ``list[smdebug.modes enum value]`` - List of modes for which data was
    saved from the training job across all steps seen.

.. method:: trial.mode(global_step=100)

  Given a global step number you can identify the mode for that step using
  this method.

  **Parameters:**

    - ``global_step (int)`` Takes the global step as an integer

  **Returns:**

    ``smdebug.modes enum value`` of the given global step

.. method:: trial.mode_step(global_step=100)

  Given a global step number you can identify the ``mode_step`` for that
  step using this method.

  **Parameters:**

    - ``global_step (int)`` Takes the global step as an integer

  **Returns:**

    ``int``: An integer representing ``mode_step`` of the given global step.
    Typically used in conjunction with ``mode`` method.

.. method:: trial.global_step(mode=modes.GLOBAL, mode_step=100)

  Given a mode and a mode_step number you can retrieve its global step
  using this method.

  **Parameters:**

    - ``mode (smdebug.modes enum value)`` Takes the mode as enum value
    - ``mode_step (int)`` Takes the mode step as an integer

  **Returns:**

    ``int`` An integer representing ``global_step`` of the given mode and
    mode_step.

.. method:: trial.workers()

  Query for all the worker processes from which data was saved by smdebug
  during multi worker training.

  **Returns:**

    ``list[str]`` A sorted list of names of worker processes from which data
    was saved. If using TensorFlow Mirrored Strategy for multi worker
    training, these represent names of different devices in the process. For
    Horovod, torch.distributed and similar distributed training approaches,
    these represent names of the form ``worker_0`` where 0 is the rank of
    the process.

.. method:: trial.collections()

  List the collections from the trial. Note that tensors part of these
  collections may not necessarily have been saved from the training job.
  Whether a collection was saved or not depends on the configuration of
  the Hook during training.

  **Returns:**

    ``dict[str -> Collection]`` - A dictionary indexed by the name of the
    collection, with the Collection object as the value. Please refer
    `Collection API <api.md#Collection>`__ for more details.

.. method:: trial.collection(coll_name)

  Get a specific collection from the trial. Note that tensors which are
  part of this collection may not necessarily have been saved from the
  training job. Whether this collection was saved or not depends on the
  configuration of the Hook during training.

  **Parameters:**

    - ``coll_name (str)`` Name of the collection

  **Returns:**

    ``Collection`` - The requested Collection object. Please refer `Collection
    API <api.html#Collection>`__ for more details.

.. method:: trial.wait_for_steps(required_steps, mode=modes.GLOBAL)

  This method allows you to wait for steps before proceeding. You might
  want to use this method if you want to wait for smdebug to see the
  required steps so you can then query and analyze the tensors saved by
  that step. This method blocks till all data from the steps are seen by
  smdebug.

  **Parameters:**

    - ``required_steps (list[int])`` Step numbers to wait for
    - ``mode (smdebug.modes enum value)`` The mode to which given step
    numbers correspond to. This defaults to modes.GLOBAL.

  **Returns:**

    None, but it only returns after we know definitely whether we have seen
    the steps.

  **Exceptions raised:**

    ``StepUnavailable`` and ``NoMoreData``. See `Exceptions <#exceptions>`__
    section for more details.

.. method:: trial.has_passed_step(step, mode=modes.GLOBAL)

  **Parameters:**

    - ``step (int)`` The step number to check if the trial has passed it
    - ``mode (smdebug.modes enum value)`` The mode to which given step
      number corresponds to. This defaults to modes.GLOBAL.

  **Returns:**

    ``smdebug.core.tensor.StepState enum value`` which can take one of three
    values ``UNAVAILABLE``, ``AVAILABLE`` and ``NOT_YET_AVAILABLE``.
