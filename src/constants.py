PATH = '/var/lib/docker/containers/be6e3c97605f2c3f49e9eb3e7773c0d22956f4a5f9352a23a62dc05edfbcfdc1/be6e3c97605f2c3f49e9eb3e7773c0d22956f4a5f9352a23a62dc05edfbcfdc1-json.log'
KEY_EVENTS = [
    'generating proof',
    'created poet client',
    'Found proof for nonce',
    'stored poet proof',
    'calculating proof of work',
    'selected the best proof',
    'poet response received',
    'awaiting atx publication epoch',
    'atx published',
    'building new atx challenge',
    'atx challenge is ready',
    'verifying the initial post',
    'loaded the initial post from disk',
    'post setup completed',
    'got poet proof',
    'Proof is invalid: numunits too large',
    'challenge submitted to poet proving service',
    'proposal eligibilities for an epoch',
    'proposalBuilder started',
    'proposal created',
    'Failed to generate proof',
    "can't recover tortoise state"
]
POET_ENDPOINTS = [
    {'endpoint': 'proofs', 'exp': 'Getting PoET Proof'},
    {'endpoint': 'pow_params', 'exp': 'Getting PoET PoW Params'},
    {'endpoint': 'submit', 'exp': 'Submitting PoST Proof'},
    {'endpoint': 'info', 'exp': 'Getting PoET Info'}
]