SMDebug Trial
=============

An SMDebug trial is an object which lets you query for tensors for a given training
job, specified by the path where SMDebug's artifacts are saved. Trial is
capable of loading new tensors as soon as they become available from the
given path, allowing you to do both offline as well as real-time
analysis.

Create an SMDebug trial object
------------------------------

Depending on the output path, there are two types of trials you can create: LocalTrial or S3Trial.
We provide a wrapper method that automatically creates the right trial.

.. autoclass::  smdebug.trials.create_trial
  :members:
  :undoc-members:
  :show-inheritance:
  :inherited-members:

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
