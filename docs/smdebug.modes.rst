Modes
-----

Used to signify which part of training you’re in, similar to Keras
modes. ``GLOBAL`` mode is used as a default when no mode was set. Choose
from

.. code:: python

   smdebug.modes.TRAIN
   smdebug.modes.EVAL
   smdebug.modes.PREDICT
   smdebug.modes.GLOBAL

The modes enum is also available under the alias
``smdebug.{framework}.modes``.
