SMDebug Trial
=============

An SMDebug trial is an object which lets you query for tensors for a given training
job, specified by the path where SMDebug's artifacts are saved. Trial is
capable of loading new tensors as soon as they become available from the
given path, allowing you to do both offline as well as real-time
analysis.

Path to SMDebug artifacts
-------------------------

To create an SMDebug trial object, you need to know where the SMDebug artifacts are saved.

1. For SageMaker training jobs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running a SageMaker job, SMDebug artifacts are saved to Amazon S3.
SageMaker saves data
from your training job to a local path of the training container and
uploads them to an S3 bucket of your account. When you start a
SageMaker training job with the python SDK, you can set the path
using the parameter ``s3_output_path`` of the ``DebuggerHookConfig``
object. If you don't specify the path, SageMaker automatically sets the
output path to your default S3 bucket.

**Example**

.. code:: python

  from sagemaker.debugger import CollectionConfig, DebuggerHookConfig

  collection_configs=[
      CollectionConfig(name="weights"),
      CollectionConfig(name="gradients")
  ]

  debugger_hook_config=DebuggerHookConfig(
    s3_output_path="specify-your-s3-bucket-uri"  # Optional
    collection_configs=collection_configs
  )

For more information, see `Configure Debugger Hook to Save Tensors
<https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-configure-hook.html>`__
in the *Amazon SageMaker Developer Guide*.

2. For non-SageMaker training jobs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are running a training job outside SageMaker, this is the path you
pass as ``out_dir`` when you create an SMDebug Hook.
When creating the hook, you can
pass either a local path (for example, ``/home/ubuntu/smdebug_outputs/``)
or an S3 bucket path (for example, ``s3://bucket/prefix``).

Create an SMDebug trial object
------------------------------

Depending on the output path, there are two types of trials you can create: LocalTrial or S3Trial.
We provide a wrapper method that automatically creates the right trial.

.. class:: smdebug.trials.create_trial(path, name=None, profiler=False, output_dir='/opt/ml/processing/outputs/', **kwargs)

  **Parameters:**

  - **path** (str): A local path or an S3 path of the form ``s3://bucket/prefix``. You should see
    directories such as ``collections``, ``events`` and ``index`` at this
    path once the training job starts.

  - **name** (str): A name for a trial.
    It is to help you manage different trials. This is an optional
    parameter, which defaults to the basename of the path if not passed.
    Please make sure to give it a unique name to prevent confusion.

  **Returns:**  An SMDebug trial instance

  The following examples show how to create an SMDebug trial object.

  **Example: Creating an S3 trial**

  .. code:: python

   from smdebug.trials import create_trial
   trial = create_trial(
     path='s3://smdebug-testing-bucket/outputs/resnet',
     name='resnet_training_run'
   )

  **Example: Creating a local trial**

  .. code:: python

   from smdebug.trials import create_trial
   trial = create_trial(
     path='/home/ubuntu/smdebug_outputs/resnet',
     name='resnet_training_run'
   )

  **Example: Restricting analysis to a range of steps**

  You can optionally pass ``range_steps`` to restrict your analysis to a
  certain range of steps. Note that if you do so, Trial will not load data
  from other steps.

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
