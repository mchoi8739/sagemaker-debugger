Hook Methods
============

Common Hook Methods
-------------------

These methods are common for all hooks in any framework.

Note that ``smd`` import below translates to
``import smdebug.{framework} as smd``.

.. list-table:: Title
  :widths: 25 25 50
  :header-rows: 1

  * - Method
    - Arguments
    - Behavior
  * - ``add_collection(collection)``
    - ``collection (smd.Collection)``
    - Takes a Collection object and adds it to the CollectionManager that the
      Hook holds. Note that you should only pass in a Collection object for the
      same framework as the hook
  * - ``get_collection(name)``
    - ``name (str)``
    - Returns collection identified by the given name
  * - ``get_collections()``
    -
    - Returns all collection objects held by the hook
  * - ``set_mode(mode)``
    - value of the enum ``smd.modes``
    - Sets mode of the job. ``smd.modes.TRAIN``,
      ``smd.modes.EVAL``, ``smd.modes.PREDICT``, ``smd.modes.GLOBAL``.
      For more information, see `Modes <#modes>`__.
  * - ``create_from_json_file(json_file_path (str)``
    - ``json_file_path (str)``
    - Takes the path of a file which holds the json configuration of the hook,
      and creates hook from that configuration. This is an optional parameter.
      If this is not passed it tries to get the file path from the value of the
      environment variable SMDEB UG_CONFIG_FILE_PATH and defaults to
      ``/opt/ml/input/config/debughookconfig.json``.
      When training on SageMaker you do not have to specify any path because
      this is the default path that SageMaker writes the hook configuration to.
  * - ``close()``
    -
    - Closes all files that are currently open by the hook
  * - ``save_scalar()``
    - ``name (str)``, ``value (float)``, ``sm_metric (bool)``
    - Saves a scalar value by the given name. Passing ``sm_metric=True`` flag also
      makes this scalar available as a SageMaker Metric to show up in SageMaker
      Studio. Note that when ``sm_metric`` is False, this scalar always resides
      only in your AWS account, but setting it to True saves the scalar also
      on AWS servers. The default value of ``sm_metric`` for this method is False.
  * - ``save_tensor()``
    - ``tensor_name (str)``, ``tensor_value (numpy.array or numpy.ndarray)``,
      ``collections_to_write (str or list[str])``
    - Manually save metrics tensors. The re cord_tensor_value() API is
      deprecated in favor or ``save_tensor()``.


TensorFlow specific Hook API
----------------------------

Note that there are three types of Hooks in TensorFlow: SessionHook,
EstimatorHook and KerasHook based on the TensorFlow interface being used
for training. `This page <tensorflow.md>`__ shows examples of each of
these.

+-----------------+-----------------+-----------------+-----------------+
| Method          | Arguments       | Returns         | Behavior        |
+=================+=================+=================+=================+
| ``wrap_optimiz  | ``optimizer``   | Returns the     | When not using  |
| er(optimizer)`` | (tf.            | same optimizer  | Zero Script     |
|                 | train.Optimizer | object passed   | Change          |
|                 | or              | with a couple   | environments,   |
|                 | tf.k            | of identifying  | calling this    |
|                 | eras.Optimizer) | markers to help | method on your  |
|                 |                 | ``smdebug``.    | optimizer is    |
|                 |                 | This returned   | necessary for   |
|                 |                 | optimizer       | SageMaker       |
|                 |                 | should be used  | Debugger to     |
|                 |                 | for training.   | identify and    |
|                 |                 |                 | save gradient   |
|                 |                 |                 | tensors. Note   |
|                 |                 |                 | that this       |
|                 |                 |                 | method returns  |
|                 |                 |                 | the same        |
|                 |                 |                 | optimizer       |
|                 |                 |                 | object passed   |
|                 |                 |                 | and does not    |
|                 |                 |                 | change your     |
|                 |                 |                 | optimization    |
|                 |                 |                 | logic. If the   |
|                 |                 |                 | hook is of type |
|                 |                 |                 | ``KerasHook``,  |
|                 |                 |                 | you can pass in |
|                 |                 |                 | either an       |
|                 |                 |                 | object of type  |
|                 |                 |                 | ``tf.tr         |
|                 |                 |                 | ain.Optimizer`` |
|                 |                 |                 | or              |
|                 |                 |                 | ``tf.ker        |
|                 |                 |                 | as.Optimizer``. |
|                 |                 |                 | If the hook is  |
|                 |                 |                 | of type         |
|                 |                 |                 | ``SessionHook`` |
|                 |                 |                 | or              |
|                 |                 |                 | ``E             |
|                 |                 |                 | stimatorHook``, |
|                 |                 |                 | the optimizer   |
|                 |                 |                 | can only be of  |
|                 |                 |                 | type            |
|                 |                 |                 | ``tf.tra        |
|                 |                 |                 | in.Optimizer``. |
|                 |                 |                 | This new        |
+-----------------+-----------------+-----------------+-----------------+
| ``add_to_       | ``collecti      | ``None``        | Calls the       |
| collection(``\  | on_name (str)`` |                 | ``add`` method  |
| ``collection_na | : name of the   |                 | of a collection |
| me, variable)`` | collection to   |                 | object. See     |
|                 | add to.         |                 | `this           |
|                 | ``variable``    |                 | section <       |
|                 | parameter to    |                 | #collection>`__ |
|                 | pass to the     |                 | for more.       |
|                 | collection’s    |                 |                 |
|                 | ``add`` method. |                 |                 |
+-----------------+-----------------+-----------------+-----------------+

The following hook APIs are specific to training scripts using the TF
2.x GradientTape
(`Example <tensorflow.md#TF%202.x%20GradientTape%20example>`__):

+-----------------+-----------------+-----------------+-----------------+
| Method          | Arguments       | Returns         | Behavior        |
+=================+=================+=================+=================+
| ``wr            | ``tape``        | Returns a tape  | When not using  |
| ap_tape(tape)`` | (t              | object with     | Zero Script     |
|                 | ensorflow.pytho | three           | Change          |
|                 | n.eager.backpro | identifying     | environments,   |
|                 | p.GradientTape) | markers to help | calling this    |
|                 |                 | ``smdebug``.    | method on your  |
|                 |                 | This returned   | tape is         |
|                 |                 | tape should be  | necessary for   |
|                 |                 | used for        | SageMaker       |
|                 |                 | training.       | Debugger to     |
|                 |                 |                 | identify and    |
|                 |                 |                 | save gradient   |
|                 |                 |                 | tensors. Note   |
|                 |                 |                 | that this       |
|                 |                 |                 | method returns  |
|                 |                 |                 | the same tape   |
|                 |                 |                 | object passed.  |
+-----------------+-----------------+-----------------+-----------------+


MXNet specific Hook API
-----------------------

+-----------------------+-----------------------+-----------------------+
| Method                | Arguments             | Behavior              |
+=======================+=======================+=======================+
| ``re                  | ``blo                 | Calling this method   |
| gister_block(block)`` | ck (mx.gluon.Block)`` | applies the hook to   |
|                       |                       | the Gluon block       |
|                       |                       | representing the      |
|                       |                       | model, so SageMaker   |
|                       |                       | Debugger gets called  |
|                       |                       | by MXNet and can save |
|                       |                       | the tensors required. |
+-----------------------+-----------------------+-----------------------+


PyTorch specific Hook API
-------------------------

+-----------------------+-----------------------+-----------------------+
| Method                | Arguments             | Behavior              |
+=======================+=======================+=======================+
| ``regi                | ``modul               | Calling this method   |
| ster_module(module)`` | e (torch.nn.Module)`` | applies the hook to   |
|                       |                       | the Torch Module      |
|                       |                       | representing the      |
|                       |                       | model, so SageMaker   |
|                       |                       | Debugger gets called  |
|                       |                       | by PyTorch and can    |
|                       |                       | save the tensors      |
|                       |                       | required.             |
+-----------------------+-----------------------+-----------------------+
| ``registe             | ``l                   | Calling this method   |
| r_loss(loss_module)`` | oss_module (torch.nn. | applies the hook to   |
|                       | modules.loss._Loss)`` | the Torch Module      |
|                       |                       | representing the      |
|                       |                       | loss, so SageMaker    |
|                       |                       | Debugger can save     |
|                       |                       | losses                |
+-----------------------+-----------------------+-----------------------+

--------------
