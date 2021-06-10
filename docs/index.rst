Welcome to the SMDebug documentation!
===============================================

|codecov| |PyPI|

.. toctree::
   :maxdepth: 2
   :caption: Introduction to SMDebug

   README
   release-notes

.. toctree::
   :maxdepth: 2
   :caption: How to Register SMDebug Hooks

   tensorflow
   pytorch
   mxnet
   xgboost

.. toctree::
  :maxdepth: 2
  :caption: Rules

  smdebug.rules

.. toctree::
  :maxdepth: 2
  :caption: SMDebug Debugging Modules

  smdebug.trials
  trial-api
  tensor-api
  smdebug.analysis

.. toctree::
  :maxdepth: 4
  :caption: SMDebug Profiler Modules

  smdebug.profiler
  smdebug.profiler.analysis
  smdebug.profiler.analysis.utils
  smdebug.profiler.analysis.notebook_utils

.. toctree::
  :maxdepth: 4
  :caption: Handling Exceptions

  smdebug.exceptions

.. |codecov| image:: https://codecov.io/gh/awslabs/sagemaker-debugger/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/awslabs/sagemaker-debugger
.. |PyPI| image:: https://badge.fury.io/py/smdebug.svg
  :target: https://badge.fury.io/py/smdebug
