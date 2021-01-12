.. smdebug-apidoc-test documentation master file, created by
   sphinx-quickstart on Fri Sep 18 22:40:22 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SMDebug test's documentation!
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
  :caption: Contents:

  smdebug.rules
  smdebug.trial
  smdebug.analysis

.. toctree::
  :maxdepth: 4

  smdebug.profiler
  smdebug.profiler.analysis
  smdebug.profiler.analysis.utils
  smdebug.profiler.analysis.notebook_utils

smdebug.exceptions module
-------------------------

.. automodule:: smdebug.exceptions
   :members:
   :undoc-members:
   :show-inheritance:


.. |codecov| image:: https://codecov.io/gh/awslabs/sagemaker-debugger/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/awslabs/sagemaker-debugger
.. |PyPI| image:: https://badge.fury.io/py/smdebug.svg
  :target: https://badge.fury.io/py/smdebug
