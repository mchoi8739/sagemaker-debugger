Configure Hook using SageMaker Python SDK
-----------------------------------------

After you make the changes to your training script, you can
configure the hook with parameters to the SageMaker Debugger API
operation, ``DebuggerHookConfig``.

.. code:: python

    from sagemaker.debugger import DebuggerHookConfig

    collection_configs=[
        CollectionConfig(name="tensor_collection_1")
        CollectionConfig(name="tensor_collection_2")
        ...
        CollectionConfig(name="tensor_collection_n")
    ]

    hook_config = DebuggerHookConfig(
        s3_output_path='s3://smdebug-dev-demo-pdx/mnist',
        collection_configs=collection_configs,
        hook_parameters={
           "parameter": "value"
        }
    )

Hook Configuration Parameter Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The available ``hook_parameters`` keys are listed in the following. The meaning
of these parameters will be clear as you review the sections of
documentation below. Note that all parameters below have to be strings.
So for any parameter which accepts a list (such as save_steps,
reductions, include_regex), the value needs to be given as strings
separated by a comma between them.

::

   dry_run
   save_all
   include_workers
   include_regex
   reductions
   save_raw_tensor
   save_shape
   save_interval
   save_steps
   start_step
   end_step
   train.save_interval
   train.save_steps
   train.start_step
   train.end_step
   eval.save_interval
   eval.save_steps
   eval.start_step
   eval.end_step
   predict.save_interval
   predict.save_steps
   predict.start_step
   predict.end_step
   global.save_interval
   global.save_steps
   global.start_step
   global.end_step
