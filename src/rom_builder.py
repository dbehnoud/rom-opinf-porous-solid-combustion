import opinf 

def train_rom(snapshot_matrix, time_vector, transformer, lifter, r=40, regularizer=1e4):
    rom = opinf.ROM(
        basis=opinf.basis.PODBasis(num_vectors=r),
        ddt_estimator=opinf.ddt.UniformFiniteDifferencer(time_vector, "ord4"),
        transformer=transformer,
        lifter=lifter,
        model=opinf.models.ContinuousModel([
            opinf.operators.ConstantOperator(),
            opinf.operators.LinearOperator(),
            opinf.operators.QuadraticOperator(),
            opinf.operators.CubicOperator()
        ], solver=opinf.lstsq.L2Solver(regularizer=regularizer))
    )
    rom.fit(snapshot_matrix)
    return rom

def train_param_rom(snapshot_matrix, parameters, time_vector, transformer, lifter, r=40, regularizer=1.2e4):
    romp = opinf.ParametricROM(
        basis=opinf.basis.PODBasis(num_vectors=r),
        ddt_estimator=opinf.ddt.UniformFiniteDifferencer(time_vector, "ord4"),
        # ddt_estimator=opinf.ddt.InterpDerivativeEstimator(time_domain=trp, InterpolatorClass= "cubic"),
        lifter= lifter,
        transformer= transformer,
        model= opinf.models.ParametricContinuousModel(
            operators=[
                opinf.operators.ConstantOperator(),
                opinf.operators.AffineLinearOperator(coeffs=lambda mu: [mu,1], nterms=2),
                opinf.operators.QuadraticOperator(),
                opinf.operators.CubicOperator()
            ],
        solver=opinf.lstsq.L2Solver(regularizer=regularizer),
        #solver=opinf.lstsq.TikhonovSolver())),
        ),
        ).fit(parameters, snapshot_matrix)
    return romp