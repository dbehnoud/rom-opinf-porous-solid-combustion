from opinf.pre import TransformerMulti, ShiftScaleTransformer

def get_combustion_transformer():

    combustion_transformer = TransformerMulti(
        transformers=[
            #opinf.pre.ShiftScaleTransformer(
            #    name="pressure", centering=True, scaling="maxabs", verbose=False
            #),
            ShiftScaleTransformer(
                name="x-velocity", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                name="y-velocity", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                name="temperature", centering=True, scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                name="s-temperature", centering=True, scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="specific volume-by-phi", centering=True, scaling="minmax", verbose=True
                name="specific volume", centering=False, scaling="maxabs", verbose=False
            ),
            # opinf.pre.ShiftScaleTransformer(
            #     # name="phi", centering=True, scaling="minmax", verbose=True
            #    name="iphi", centering=True, scaling="maxabs", verbose=False
            # ),
            ShiftScaleTransformer(
                #name="methane", scaling="minmax", verbose=True
                name="methane", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="oxygen", scaling="minmax", verbose=True
                name="oxygen", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="water", scaling="minmax", verbose=True
                name="water", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="carbon dioxide", scaling="minmax", verbose=True
                name="carbon dioxide", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="carbon monoxide", scaling="minmax", verbose=True
                name="carbon monoxide", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="nitrogen", scaling="minmax", verbose=True
                name="nitrogen", scaling="maxabs", verbose=False
            ),
            # opinf.pre.ShiftScaleTransformer(
            #     #name="ngas", scaling="minmax", verbose=True
            #     name="ngas", scaling="maxabs", verbose=False
            # ),
            ShiftScaleTransformer(
                #name="wood", scaling="minmax", verbose=True
                name="wood", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="char", scaling="minmax", verbose=True
                name="char", scaling="maxabs", verbose=False
            )
        ]
    )
    return combustion_transformer