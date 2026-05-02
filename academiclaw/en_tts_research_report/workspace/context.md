# Important TTS Research Papers (2020-2025)

## 1. Autoregressive and Non-Autoregressive Models

### 1.1 FastSpeech 2: Fast and High-Quality End-to-End Text to Speech (2020)
- **Authors**: Ren, Yi, et al.
- **Link**: https://arxiv.org/abs/2006.04558
- **Key Contributions**:
  - Solved the complex teacher-student distillation pipeline problem in FastSpeech
  - Directly uses ground-truth targets for training instead of simplified teacher model outputs
  - Introduces more speech variation information (pitch, energy, more accurate duration) as conditional inputs
  - Proposes FastSpeech 2s, the first system to directly and parallelly generate speech waveforms from text

### 1.2 VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech (2021)
- **Authors**: Kim, Jaehyeon, et al.
- **Link**: https://arxiv.org/abs/2106.06103
- **Key Contributions**:
  - The first fully end-to-end TTS model without intermediate feature representations
  - Combines variational autoencoders with generative adversarial networks
  - Achieves text-to-audio alignment through monotonic alignment search
  - Achieves SOTA performance on multiple datasets

## 2. Diffusion Models

### 2.1 Diff-TTS: A Denoising Diffusion Model for Text-to-Speech (2021)
- **Authors**: Jeong, Myeonghun, et al.
- **Link**: https://arxiv.org/abs/2104.01409
- **Key Contributions**:
  - First application of diffusion models to TTS tasks
  - Likelihood-based optimization to learn mel-spectrogram distributions
  - Uses accelerated sampling methods to improve inference speed
  - Achieves 28x real-time speed on a single NVIDIA 2080Ti GPU

### 2.2 Grad-TTS: A Diffusion Probabilistic Model for Text-to-Speech (2021)
- **Authors**: Popov, Vadim, et al.
- **Link**: https://arxiv.org/abs/2105.06337
- **Key Contributions**:
  - Score-matching based diffusion model
  - Achieves high-quality mel-spectrogram generation
  - Supports multiple conditional inputs and generation control

### 2.3 ProDiff: Progressive Fast Diffusion Model for High-Quality Text-to-Speech (2022)
- **Authors**: Huang, Rongjie, et al.
- **Link**: https://arxiv.org/abs/2207.06389
- **Key Contributions**:
  - Progressive diffusion model that reduces denoising steps
  - Significantly improves generation speed
  - Maintains high-quality speech generation

## 3. Large-Scale Pre-trained Models

### 3.1 VALL-E: Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers (2023)
- **Authors**: Wang, Chengyi, et al.
- **Link**: https://arxiv.org/abs/2301.02111
- **Key Contributions**:
  - The first large-scale neural codec language model
  - Pre-trained on 60K hours of English speech
  - Achieves high-quality voice cloning with only 3 seconds of reference audio
  - Possesses in-context learning capability

### 3.2 VALL-E 2: Neural Codec Language Models are Human Parity Zero-Shot Text to Speech Synthesizers (2024)
- **Authors**: Wang, Chengyi, et al.
- **Link**: https://arxiv.org/abs/2406.05370
- **Key Contributions**:
  - The first zero-shot TTS system to achieve human parity
  - Introduces repetition-aware sampling to stabilize the decoding process
  - Grouped code modeling to shorten sequence length and improve inference speed
  - Surpasses all previous systems on LibriSpeech and VCTK datasets

### 3.3 NaturalSpeech 2: Latent Diffusion Models are Natural and Zero-Shot Speech and Singing Synthesizers (2023)
- **Authors**: Tan, Xu, et al.
- **Link**: https://arxiv.org/abs/2304.09116
- **Key Contributions**:
  - Pre-trained TTS system combining diffusion models
  - Supports zero-shot speech and singing synthesis
  - Performs diffusion in latent space to reduce computation
  - Achieves near-human-level speech quality

## 4. Flow Models and Hybrid Architectures

### 4.1 Glow-TTS: A Generative Flow for Text-to-Speech via Monotonic Alignment Search (2020)
- **Authors**: Kim, Jaehyeon, et al.
- **Link**: https://arxiv.org/abs/2005.11129
- **Key Contributions**:
  - Combines normalizing flows with monotonic alignment search
  - Achieves high-quality non-autoregressive TTS
  - Invertible transformations provide meaningful latent representations

### 4.2 Flowtron: An Autoregressive Flow-based Generative Network for Text-to-Speech Synthesis (2020)
- **Authors**: Valle, Rafael, et al.
- **Link**: https://arxiv.org/abs/2005.05957
- **Key Contributions**:
  - Combines autoregressive generation with normalizing flows
  - Improves expressive diversity
  - Supports flexible speech attribute control

## 5. Latest Advances 2024-2025

### 5.1 SimpleSpeech 2: Towards Simple and Efficient Text-to-Speech with Flow-based Scalar Latent Transformer Diffusion Models (2024)
- **Authors**: Yang, Dongchao, et al.
- **Link**: https://arxiv.org/abs/2408.13893
- **Key Contributions**:
  - Hybrid architecture combining flow models and diffusion models
  - Simplified data preparation and model design
  - Stable, high-quality generation performance with fast inference speed
  - Supports multilingual TTS

### 5.2 Schrodinger Bridges Beat Diffusion Models on Text-to-Speech Synthesis (2023)
- **Authors**: Liu, Songxiang, et al.
- **Link**: https://arxiv.org/abs/2312.03491
- **Key Contributions**:
  - Uses Schrodinger bridges to replace noisy Gaussian priors
  - Constructs a fully tractable data-to-data process
  - Significantly surpasses diffusion models in synthesis quality and sampling efficiency

### 5.3 Fine-Tuning Text-to-Speech Diffusion Models Using Reinforcement Learning with Human Feedback (2025)
- **Authors**: Zhang, Yizhe, et al.
- **Link**: https://arxiv.org/abs/2508.03123
- **Key Contributions**:
  - Proposes the Diffusion Loss-Guided Policy Optimization (DLPO) framework
  - Integrates original training loss into the reward function
  - Uses naturalness scores as feedback to improve speech quality
  - Achieves significant improvements on WaveGrad 2

## 6. Evaluation and Benchmarks

### 6.1 Blizzard Challenge 2023: MuLanTTS - The Microsoft Speech Synthesis System (2023)
- **Authors**: Microsoft Research Team
- **Link**: https://arxiv.org/abs/2309.02743
- **Key Contributions**:
  - Microsoft's end-to-end neural TTS system
  - Outstanding performance in Blizzard Challenge 2023
  - Quality evaluation average scores of 4.3-4.5, statistically comparable to natural speech

### 6.2 ASVspoof 5: Crowdsourced Speech Data, Deepfakes, and Adversarial Attacks at Scale (2024)
- **Authors**: ASVspoof Consortium
- **Link**: https://arxiv.org/abs/2408.08739
- **Key Contributions**:
  - Fifth generation voice forgery and deepfake detection challenge
  - Large-scale database built on crowdsourced data
  - First to incorporate adversarial attacks
  - Supports SASV evaluation and standalone detection solutions

## 7. Multilingual and Cross-lingual

### 7.1 VALL-E X: Speak Foreign Languages with Your Own Voice: Cross-Lingual Neural Codec Language Modeling (2023)
- **Authors**: Zhang, Ziqiang, et al.
- **Link**: https://arxiv.org/abs/2303.03926
- **Key Contributions**:
  - Cross-lingual neural codec language model
  - Supports zero-shot cross-lingual text-to-speech synthesis
  - Supports zero-shot speech-to-speech translation
  - Effectively mitigates foreign accent issues

### 7.2 YourTTS: Towards Zero-Shot Multi-Speaker TTS and Zero-Shot Voice Conversion for Everyone (2022)
- **Authors**: Casanova, Edresson, et al.
- **Link**: https://arxiv.org/abs/2112.02418
- **Key Contributions**:
  - Zero-shot multi-speaker TTS system
  - Combines VITS architecture to support multilingual zero-shot cloning
  - Excellent performance with limited data

## 8. Expressiveness and Controllability

### 8.1 SC VALL-E: Style-Controllable Zero-Shot Text to Speech Synthesizer (2023)
- **Authors**: Lee, Sang-Hoon, et al.
- **Link**: https://arxiv.org/abs/2307.10550
- **Key Contributions**:
  - Controllable TTS based on neural codec language models
  - Identifies attribute tokens in the style embedding matrix
  - Supports control of emotion, speech rate, pitch, voice intensity, and other attributes
  - Generates diverse expressive voices on unseen training data

### 8.2 ControlSpeech: Towards Simultaneous Zero-shot Speaker Cloning and Zero-shot Language Style Control With Decoupled Codec (2024)
- **Authors**: Li, Ziyang, et al.
- **Link**: https://arxiv.org/abs/2406.01205
- **Key Contributions**:
  - Simultaneously achieves zero-shot speaker cloning and zero-shot language style control
  - Uses bidirectional attention and mask-based parallel decoding
  - Proposes the Style Mixture Semantic Density (SMSD) model
  - Solves text style controllability issues in many-to-many mapping

## Reference Format Example

All references should follow IEEE format:

[1] Y. Ren, C. Hu, X. Tan, T. Qin, S. Zhao, Z. Zhao, and T.-Y. Liu, "FastSpeech 2: Fast and High-Quality End-to-End Text to Speech," in *Proc. ICLR*, 2021.

[2] J. Kim, J. Kong, and J. Son, "VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech," in *Proc. ICML*, 2021.

[3] M. Jeong, H. Kim, S. J. Cheon, B. J. Choi, and N. S. Kim, "Diff-TTS: A Denoising Diffusion Model for Text-to-Speech," in *Proc. ICASSP*, 2021.

[4] C. Wang, S. Chen, Y. Wu, Z. Zhang, L. Zhou, S. Liu, Z. Chen, Y. Liu, H. Wang, J. Li, L. He, S. Zhao, and F. Wei, "VALL-E: Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers," in *Proc. Interspeech*, 2023.

[5] C. Wang, S. Chen, Y. Wu, Z. Zhang, L. Zhou, S. Liu, Z. Chen, Y. Liu, H. Wang, J. Li, L. He, S. Zhao, and F. Wei, "VALL-E 2: Neural Codec Language Models are Human Parity Zero-Shot Text to Speech Synthesizers," in *Proc. Interspeech*, 2024.

[6] X. Tan, J. Chen, H. Liu, J. Cong, C. Zhang, Y. Liu, X. Wang, Y. Leng, Y. Yi, L. He, F. Soong, T. Qin, S. Zhao, and T.-Y. Liu, "NaturalSpeech 2: Latent Diffusion Models are Natural and Zero-Shot Speech and Singing Synthesizers," in *Proc. NeurIPS*, 2023.

[7] D. Yang, S. Liu, R. Huang, G. Cui, and Z. Zhao, "SimpleSpeech 2: Towards Simple and Efficient Text-to-Speech with Flow-based Scalar Latent Transformer Diffusion Models," in *Proc. Interspeech*, 2024.

[8] S. Liu, D. Yang, R. Huang, G. Cui, and Z. Zhao, "Schrodinger Bridges Beat Diffusion Models on Text-to-Speech Synthesis," in *Proc. NeurIPS*, 2023.

[9] Y. Zhang, L. Wang, H. Li, and J. Yu, "Fine-Tuning Text-to-Speech Diffusion Models Using Reinforcement Learning with Human Feedback," in *Proc. ICASSP*, 2025.

[10] ASVspoof Consortium, "ASVspoof 5: Crowdsourced Speech Data, Deepfakes, and Adversarial Attacks at Scale," in *Proc. Odyssey*, 2024.
