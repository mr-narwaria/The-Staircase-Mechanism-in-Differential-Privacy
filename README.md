## The Staircase Mechanism in Differential

Laplacian noise is a standard way to add noise to data to sanitize numerical data in 
differential privacy mechanisms before publishing it. In this paper, the author proposes 
another noise-adding called staircase mechanism for differential privacy. He has shown that 
the staircase mechanism can replace the Laplace mechanism and improve performance, 
particularly in medium and low privacy regimes. The staircase mechanism is proven to be the 
optimal noise-adding mechanism in a universal context, subject to a conjectured technical 
lemma. The paper also discusses that we can balance accuracy and privacy by using staircase 
mechanisms in differential privacy.

## Dependencies
- virtualenv
  ```bash
  pip install virtualenv
  ```
- pandas
- matplotlib
- diffprivlib

## How to Run
### Create a Virtual Environment for package installation
1. Goto to the main directory of your project
2. Create a virtual environment using virtualenv package
```bash
  virtualenv venv
```
3. Activate Virtual Environment
 ```bash
    venv\Scripts\activate
  ```
### Install Require Dependencies
```bash
  pip install pandas
```
```bash
  pip install matplotlib
```
```bash
  pip install diffprivlib
```
### For Comparison between Laplace and Staircase Mechanisms
1. Install the Dependacies
2. Run this command in the terminal
```bash
    python compare.py
```
It gives output as a graph of comparison between Laplace and Staircase Mechanisms.

### For Accuracy of Laplace and Staircase Mechanisms
1. Install the Dependacies
2. Run this command in the terminal
```bash
    python accuracy.py
```
It gives an output of an accuracy graph between Laplace and Staircase mechanisms.

## Authors

- [Shambhoolal Narwaria](https://github.com/mr-narwaria)
