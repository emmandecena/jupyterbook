using JuMP, Clp


m = Model(Clp.Optimizer)

@variable(m, 0<= x <=40)
@variable(m, y <=0)
@variable(m, z <=0)
@objective(m, Max, x + y + z)

@constraint(m, const1, -x +  y + z <= 20)
@constraint(m, const2,  x + 3y + z <= 30)

optimize!(m)
println("Optimal Solutions:")
println("x = ", getvalue(x))
println("y = ", getvalue(y))
println("z = ", getvalue(z))



