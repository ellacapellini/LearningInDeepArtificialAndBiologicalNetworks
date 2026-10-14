**************************************************
Tutorial on Backpropagation and Feedback-Alignment
**************************************************

.. Comment: Only the README content after the inclusion marker below will be added to the documentation by sphinx.
.. content-inclusion-marker-do-not-remove

In tutorial 2.1, you will be implementing parts of the backpropagation algorithm by completing missing parts in the module :mod:`lib.backprop_functions`. Tutorial 2.2 is similar in spirit, but you will modify your implementations of the backward pass in :mod:`lib.feedback_alignment_functions` to implement the Feedback-Alignment_ (FA) algorithm. Please scroll down for extra information on tutorial 2.1 and 2.2.

Tutorial 2.1
##########################

In the first tutorial session of this exercise, you have seen how to derive the backpropagation update rules. In this exercise, you are going to implement the forward and backward pass for core blocks that are often used in Artificial Neural Networks.

Please refer to the :ref:`API <api-reference-label>` to get an overview of the coding structure.

You can test your implementations by following the instructions from the :ref:`testing <tests-reference-label>` page.

In addition, you can see your code in action by learning a simple regression task via the script :mod:`main`. Please study the command-line arguments on how to use the script.

.. code-block:: console

  $ python3 main.py --help

To visually certify the quality of the obtained predictions, you can visualize the results of a 1D regression task via

.. code-block:: console

  $ python3 main.py --polynomial_regression --show_plot --epochs=1000 --lr=1e-2
  
We recommend playing around with command-line options such as learning rate ``--lr``, momentum ``--momentum``, the number of epochs ``--epochs`` or the batch size ``--batchsize`` as well as the architectural options of the neural network to get a feeling for how optimization with backpropagation in neural networks behaves.

Tutorial 2.2
##############################
In the second tutorial session, we explained why Feedback-Alignment_ works and why it can be seen as a more biologically plausible variant of error-backpropagation. In this exercise, you are going to implement feedback alignment and investigate some simple toy examples to get more insight in the inner workings of Feedback-Alignment_.

Please refer to the :ref:`API <api-reference-label>` to get an overview of the coding structure.

Below, we give you the needed commandline code for running the experiments of tutorial 2.2.

Linear student-teacher regression with feedback alignment:

.. code-block:: console

  $ python3 main.py --size_hidden 20 --size_input 30 --size_output 10 --num_hidden 1 --lr 1.e-1 --epochs 200 --feedback_alignment --plot_matrix_angles --linear

Nonlinear student-teacher regression with feedback alignment:

.. code-block:: console

  $ python3 main.py  --size_hidden 20 --size_input 30 --size_output 10 --num_hidden 1 --lr 3e-1 --epochs 300 --feedback_alignment --plot_matrix_angles

Nonlinear student-teacher regression with backpropagation:

.. code-block:: console

  $ python3 main.py  --size_input 30 --size_hidden 20 --size_output 10 --num_hidden 1 --lr 3e-1 --epochs 300

Polynomial regression with feedback alignment:

.. code-block:: console

  $ python3 main.py --polynomial_regression --show_plot --epochs=20000 --lr=2e-1 --feedback_alignment

Polynomial regression with backpropagation:

.. code-block:: console

  $ python3 main.py --polynomial_regression --show_plot --epochs=20000 --lr=2e-2






**Please refer to the assignment sheet to obtain further information on how exercises have to be handed in and how they are graded. Note that you need to submit three files in total: backprop_functions.py, feedback_alignment_functions.py and a pdf file with the answers on the questions of tutorial 2.2.**

.. _Feedback-Alignment: https://www.nature.com/articles/ncomms13276
