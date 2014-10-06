"""
GLM connected by a sparse network and Gaussian weights.
"""
SparseWeightedModel = \
{
    # Number of neurons (parametric model!)
    'N' : 1,
    
    # Parameters of the nonlinearity
    'nonlinearity' :
        {
            'type' : 'explinear'
        },
    
    # Parameters of the bias    
    'bias' :
        {
            'type' : 'constant',
            'mu' : 20.0,
            # 'mu' : 1.0,
            'sigma' : 0.25
        },

    # Parameters of the background model
    'bkgd' :
        {
            #'type' : 'basis',
            'type' : 'no_stimulus',
            'D_stim' : 1,       # Dimensionality of the stimulus
            'dt_max' : 0.3,
            'mu' : 0,
            'sigma' : 0.5,
            'basis' :
                {
                    'type' : 'cosine',
                    'n_eye' : 0,
                    'n_cos' : 3,
                    'a': 1.0/120,
                    'b': 0.5,
                    'orth' : False,
                    'norm' : True
                }
        },

    # Parameters of the impulse responses
    'impulse' :
        {
            # 'type' : 'normalized',
            'type' : 'dirichlet',
            'dt_max' : 0.2,
            'alpha' : 1,
            'basis' :
                {
                    'type' : 'cosine',
                    'n_eye' : 0,
                    'n_cos' : 5,
                    #'type' : 'exp',
                    #'n_eye' : 0,
                    #'n_exp' : 5,
                    'a': 1.0/120,
                    'b': 0.5,
                    'orth' : False,
                    'norm' : True
                }
        },

    # Parameters of the network
    'network' :
        {
            'weight' :
                {
                    'type' : 'gaussian',
                    'prior' : 
                     {
                         'type' : 'gaussian',
                         'mu' : 0.0,
                         'sigma' : 1.0
                         # 'sigma' : 0.1
                     },
                    'refractory_prior' :
                    {
                        'type' : 'gaussian',
                        # 'mu' : -0.2,
                        'mu' : -1.0,
                        # 'mu' : 0.0,
                        'sigma' : 0.5
                        # 'sigma' : 0.1
                    }
                },

            'graph' :
                {
                    'type' : 'erdos_renyi',
                    'rho' : 0.5,
                    'rho_refractory' : 1.0
                }
        },
}


