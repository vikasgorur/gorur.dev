module Mandelbrot

export mandelbrot

function mandelbrot(c::Complex, maxiter::Int)
    z = c
    for n in 1:maxiter
        if abs(z) > 2
            return n-1
        end
        z = z*z + c
    end
    return maxiter
end

end