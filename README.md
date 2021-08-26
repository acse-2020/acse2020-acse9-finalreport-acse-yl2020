<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/acse-2020/">
    <img src="readme_files/logo_imperial_college_london.png" alt="Logo" width="270" height="100">
  </a>
  
  <h3 align="center">Final project</h3>
  <p align="center">
    
  </p>
</p>


## Data assimilation using Generative Adversarial Networks to determine COVID-19 infection risks in enclosed spaces using autoencoders for compression

## Project Description

This project contains to apply AI model that is built on the results from CFD simulations to predict the CO2 distribution within a room based on CO2 sensor data that is limited and observations from field campaign based on different non-linear dimensionality reduction methods, and it is combined with data from sensors that are located in optimal spatial locations to improve accuracy of the models from AE-based ROMs to predict the risk of airborne COVID infection within a room. The project is built based on the work DA-PredGAN(https://arxiv.org/abs/2105.07729), SFC-CAE(https://arxiv.org/abs/2011.14820) and SVD-AE(https://arxiv.org/abs/2008.10532).

## Getting started
### Dependencies

* Python ~= 3.8.5
* torch >= 1.8.0
* Tensorflow >= 2.0
* numpy >= 1.19.5
* matplotlib ~= 3.2.2
* vtk >= 9.0
* livelossplot ~= 0.5.4
* meshio[all]
* cmocean ~= 2.0

* progressbar2 ~= 3.38.0
* (Optional) GPU/multi GPUs with CUDA

## Template Notebooks

### [SVD-AE, PCA, NMF with GAN training]()


###[PredGAN]()

### [SFC-CAE](PredGAN/SFC-CAE/SFC_CAE_Compression.ipynb)


### [T-SNE visualisation of latent variables](t_SNE_visualisation.ipynb)

## License

Distributed under the Apache 2.0 License.

## Testing 
Some basic tests for the module are avaliable in the .ipynb files.

## Contact
* Yushen Lin yl2020@imperial.ac.uk

## Acknowledgements
Would like to thanks my supervisors for the guides:
* Dr. Claire Heaney
* Prof. Christopher Pain 
