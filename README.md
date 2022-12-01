<div>
<img src="fig/logo.png" align="left" style="margin: 10 10 10 10;" height="100px">
	<h1> MouseGAN++ </h1>
<blockquote> Unsupervised Disentanglement and Contrastive Representation for Multiple MRI Modalities Synthesis and Structural Segmentation of Mouse Brain
</blockquote>
</div>
<br />

<hr />


### [Paper](#citation) | [Usage demo](#Usage-demo)  | [Replicate demo](#replicate-demo-and-results) | [MRI data release](/demo#dataset-release) | [Pretrained weight](/demo#pretrained-weight) | [Documentation](https://mousegan-pp.readthedocs.io)  | [Contents](#Quick-Start-Contents) | [See also: BEN](https://github.com/yu02019/BEN)

See also:
<img src="https://github.com/yu02019/BEN/blob/main/fig/logo.png" width = "100" height = "72" alt="BEN logo" align=center /> | [Github project link](https://github.com/yu02019/BEN)

```
"BEN: a generalizable Brain Extraction Net for multimodal MRI data from rodents, nonhuman primates, and humans." bioRxiv (2022).
```

---

![](fig/MouseGAN-pp-workflow.png)




### Usage Demo

| Name       | Modality                 | Colab link                                                                                                                                                          |
|------------|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MouseGAN++ | T1w, T2w, T2*w, QSM, Mag | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1IqWeyO7eLb0phOkUnBEuD4bD5napD-k-?usp=sharing) |
| MouseGAN++ |         T1w, T2w         | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1hCkeV_stkbZlS1e2QG1gMFVrpexjFgfZ?usp=sharing) |



### Replicate Demo and More Results
 

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
* numpy == 1.19
* SimpleITK == 2.0
* opencv-python == 4.2

[//]: # (* scikit-image == 0.16.2)


Install dependencies:

[//]: # (conda env export > environment.yml  &#40;Export the active environment to a new file&#41;)

```shell
git clone https://github.com/yu02019/MouseGAN-pp.git
cd MouseGAN-pp
conda env create -f environment.yml
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


- [x] ~~Update interfaces (Before October 12th)~~
- [x] ~~Update Documentation (Before October 18th)~~
- [x] ~~Update Colab demo (Before October 13th)~~
- [x] ~~Update Tutorials (Before October 16th) (see details in demo)~~
- [ ] Rewrite dataloader 
- [ ] Consolidate [`BEN`](https://github.com/yu02019/BEN) and [`MouesGAN++`](https://github.com/yu02019/MouseGAN-pp) as one fully end-to-end pipeline for the mouse brain.



# Resources


## Dataset release / Pretrained weight / Contributing to MouseGAN++

We will release our multi-modality MR mouse dataset images for more extensive communities for both neuroscience and deep learning.

The details can be found in this [folder](/demo).



---



# Citation
If you find our work / datasets useful for your research, please consider citing:

```bibtex
@ARTICLE{9966838,
  author={Yu, Ziqi and Han, Xiaoyang and Zhang, Shengjie and Feng, Jianfeng and Peng, Tingying and Zhang, Xiao-Yong},
  journal={IEEE Transactions on Medical Imaging}, 
  title={MouseGAN++: Unsupervised Disentanglement and Contrastive Representation for Multiple MRI Modalities Synthesis and Structural Segmentation of Mouse Brain}, 
  year={2022},
  volume={},
  number={},
  pages={1-1},
  doi={10.1109/TMI.2022.3225528}}
```


[//]: # (Acknowledgements: TODO)

Disclaimer: This toolkit is only for research purpose. If used on an additional dataset, the model might need to be fine-tuned before running (refer to [Limitation](/demo/README.md/#Limitation)).

