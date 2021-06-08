Welcome to the SMDebug documentation!
===============================================

|codecov| |PyPI|

.. toctree::
   :maxdepth: 2
   :caption: Introduction to SMDebug:

   README

.. toctree::
   :maxdepth: 2
   :caption: SMDebug Hooks for Frameworks:

   tensorflow
   pytorch
   mxnet
   xgboost

.. toctree::
  :maxdepth: 2
  :caption: SMDebug Rule Modules:

  smdebug.rules

.. toctree::
  :maxdepth: 2
  :caption: SMDebug Modules for Output Parameter Analysis:
  smdebug.trials
  smdebug.analysis

.. toctree::
  :maxdepth: 4
  :caption: SMDebug Modules for Profiler:

  smdebug.profiler
  smdebug.profiler.analysis
  smdebug.profiler.analysis.utils
  smdebug.profiler.analysis.notebook_utils
  smdebug.exceptions

.. |codecov| image:: https://codecov.io/gh/awslabs/sagemaker-debugger/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/awslabs/sagemaker-debugger
.. |PyPI| image:: https://badge.fury.io/py/smdebug.svg
  :target: https://badge.fury.io/py/smdebug
