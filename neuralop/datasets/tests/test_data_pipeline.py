from ..data_pipeline import DNEPipeline
from ..output_encoder import UnitGaussianNormalizer
from ..transforms import PositionalEmbedding
import torch
from torch.testing import assert_close

def test_DNEPipeline():
    if torch.backends.cuda.is_built():
        device = 'cuda'
    else:
        device='cpu'

    x = torch.randn((1,2,64,64))
    y = torch.randn((1,2,64,64))

    pos_encoder = PositionalEmbedding(grid_boundaries=[[0,1],[0,1]],
                                    channel_dim=1)
    normalizer = UnitGaussianNormalizer(mean=torch.zeros((1,2,1,1)),
                                        std=torch.ones((1,2,1,1)),
                                        eps=1e-5)

    pipeline = DNEPipeline(in_normalizer=normalizer,
                           out_normalizer=normalizer,
                           pos_encoding=pos_encoder,
                           device=device)
    
    data = {'x':x, 'y':y} # data on cpu at this point

    xform_data = pipeline.preprocess(data)

    # model outputs will be on device by default
    out = torch.randn((1,2,64,64)).to(device) 
    
    _, inv_xform_data = pipeline.postprocess(out, xform_data)

    assert_close(inv_xform_data['y'].cpu(), data['y'])