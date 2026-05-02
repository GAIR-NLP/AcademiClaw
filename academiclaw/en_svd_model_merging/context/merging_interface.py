# --- START OF FILE merging_interface.py ---
import torch
from typing import List, Dict

"""
Assignment: Isotropic Model Merging Implementation
Please implement the two functions below corresponding to Iso-C and Iso-CTS algorithms.

Constraints:
1. Input: 
   - ptm_state_dict: Dictionary of the pre-trained model weights.
   - ft_state_dicts: List of dictionaries, each containing a fine-tuned model's weights.
   - parameters: Hyperparameters (alpha, scaling coefficient, etc).
   
2. Logic:
   - Calculate Task Vectors: tau_i = theta_i - theta_0
   - Apply SVD-based merging ONLY on 2D parameter tensors (e.g., Linear weights).
   - Apply simple Task Arithmetic (Average) on 0D/1D parameter tensors (e.g., Bias, LayerNorm).
   - Return the merged state_dict.

3. Do NOT implement file I/O. Focus only on the tensor operations.
"""

def iso_c_merging(
    ptm_state_dict: Dict[str, torch.Tensor],
    ft_state_dicts: List[Dict[str, torch.Tensor]],
    alpha: float = 1.3
) -> Dict[str, torch.Tensor]:
    """
    Algorithm 1: Isotropic Merging in Common Subspace (Iso-C)
    
    Args:
        ptm_state_dict: Pre-trained model weights
        ft_state_dicts: List of fine-tuned model weights
        alpha: Scaling coefficient
        
    Returns:
        merged_state_dict: The final merged model weights
    """
    # TODO: Implement Iso-C here
    pass


def iso_cts_merging(
    ptm_state_dict: Dict[str, torch.Tensor],
    ft_state_dicts: List[Dict[str, torch.Tensor]],
    alpha: float = 1.4,
    common_ratio: float = 0.8
) -> Dict[str, torch.Tensor]:
    """
    Algorithm 2: Isotropic Merging with Common and Task-Specific Subspaces (Iso-CTS)
    
    Args:
        ptm_state_dict: Pre-trained model weights
        ft_state_dicts: List of fine-tuned model weights
        alpha: Scaling coefficient
        common_ratio: The ratio of dimensions allocated to the common subspace (k/r)
        
    Returns:
        merged_state_dict: The final merged model weights
    """
    # TODO: Implement Iso-CTS here
    pass
# --- END OF FILE merging_interface.py ---