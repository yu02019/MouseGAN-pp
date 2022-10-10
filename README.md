<div>
<img src="fig/logo.png" align="left" style="margin: 10 10 10 10;" height="100px">
	<h1> MouseGAN++ </h1>
<blockquote> Unsupervised Disentanglement and Contrastive Representation for Multiple MRI Modalities Synthesis and Structural Segmentation of Mouse Brain
</blockquote>
</div>
<br />

<hr />


### [Paper](#citation) | [Pipeline](#pipeline-demo)  | [Replicate demo](#replicate-demo-and-results) | [MRI data release](/demo) | [Pretrained weight](/demo) | [Documentation](todo)  | [Contents](#Quick-Start-Contents) | [See also: BEN](https://github.com/yu02019/BEN)

See also:
<img src="https://github.com/yu02019/BEN/blob/main/fig/logo.png" width = "100" height = "72" alt="BEN logo" align=center /> | [Github project link](https://github.com/yu02019/BEN)

```
"BEN: a generalizable Brain Extraction Net for multimodal MRI data from rodents, nonhuman primates, and humans." bioRxiv (2022).

```

---

![](fig/MouseGAN-pp-workflow.png)



[//]: # (## Overview)

[//]: # (🚀 Quick start to use BEN or replicate our experiments in 5 minutes!)

### Pipeline Demo

[//]: # (todo ! on Colab?)

| Name       | Description         | Colab link                              |
|------------|---------------------|-----------------------------------------|
| MouseGAN++ | MouseGAN++ pipeline | [link](#plan-list) (refer to plan list) |


### Replicate Demo and Results
 

| Name                      | Description                                                           | Details        |
|---------------------------|-----------------------------------------------------------------------|----------------|
| MRM NeAt segmentation     | Segmentation results & pretrained weights.                            | [link](./demo) |
| Ablation study loss curve | Loss curve for ablation study from Tensorboard.                       | [link](./demo) |
| Pretrained weight         | Pretrained weight for MouseGAN++.                                     | [link](./demo) |
| More examples             | More results of MouseGAN++ and SOTA methods, including failure cases. | [link](./demo) |
| Rater study               | Qualitatively results of synthesized images by medical experts.       | [link](./demo) |

 


---
## Quick Start Contents

Visit our [documentation](todo) for installation, tutorials and more.

* [Installation](#installation)
* [Quick Start / Tutorial](#quick-start)
    + [Run translation alone](#run-translation)
    + [Run segmentation alone](#run-segmentation)  
    + [Choice of pretext task](#choice-of-pretext-task)
    + [Plan list](#plan-list)
* [Resources](#resources)
  * [Dataset release](/dataset_release)
  * [Pretained weight](/dataset_release)



## Installation

[//]: # (An Nvidia GPU is needed for faster inference &#40;less than 1 sec/scan on 1080ti gpu&#41;.)

Requirements:

* torch == 1.3
* numpy == 1.16
* SimpleITK == 2.0
* opencv-python == 4.1

[//]: # (* scikit-image == 0.16.2)


Install dependencies:

```shell
git clone https://github.com/yu02019/MouseGAN-pp.git
cd MouseGAN-pp
pip install -r requirement.txt
```



## Run translation
For multi-modality dataset:

```shell
python translation.py --dataroot DATAROOT --name NAME --num_domains NUM_DOMAINS --out_dir OUT_DIR --resume MODEL_DIR --num NUM_PER_IMG
```


## Run segmentation
For example, run on MRM NeAt dataset:

[//]: # (todo)
```shell
python segmentation.py -i input_folder -o output_folder -w model_weight 
```

## Choice of pretext task

In our paper, we used modality translation as our pretext task, as we wanted to impute missing modality. However, if readers are faced with multi-center single modality data (e.g, T2w MR images from 11.7T and 9.4T scanners), our pretext task could change to center-style translation easily.

## Plan list


- [ ] Update interfaces (Before October 12th)
- [ ] Update Documentation (Before October 18th)
- [ ] Update Colab demo (Before October 13th)
- [ ] Update Tutorials (Before October 16th)



# Resources


## Dataset release / Pretrained weight / Contributing to MouseGAN++

We will release our multi-modality MR mouse dataset images for more extensive communities for both neuroscience and deep learning.

The details can be found in this [folder](/dataset_release).



---



# Citation
If you find our work / datasets useful for your research, please consider citing:

```bibtex
"MouseGAN++: Unsupervised Disentanglement and Contrastive Representation for Multiple MRI Modalities Synthesis and Structural Segmentation of Mouse Brain." Under review (2022)
```


[//]: # (Acknowledgements: TODO)

Disclaimer: This toolkit is only for research purpose. If used on an additional dataset, the model might need to be fine-tuned before running (refer to [Limitation](/demo/README.md/#Limitation)).

