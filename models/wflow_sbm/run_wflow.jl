#!/usr/bin/env julia
# ============================================================================
# Wflow SBM Simulation Runner
# ============================================================================
# Usage: julia run_wflow.jl <path_to_config.toml>
#
# This script executes a Wflow hydrological simulation and provides
# diagnostic output for validation.
# ============================================================================

using Wflow
using Printf

function main()
    println("=" ^ 60)
    println("Wflow SBM Hydrological Simulation")
    println("=" ^ 60)
    println()

    # Validate arguments
    if length(ARGS) != 1
        println("Usage: julia run_wflow.jl <path_to_wflow_sbm.toml>")
        println()
        println("Example:")
        println("  julia run_wflow.jl wflow_niger/wflow_sbm.toml")
        exit(1)
    end

    config_path = ARGS[1]

    # Check config exists
    if !isfile(config_path)
        println("ERROR: Configuration file not found: $config_path")
        exit(1)
    end

    println("Configuration: $config_path")
    println("Output directory: $(dirname(config_path))/run_default")
    println()

    # Run simulation with timing
    println("Starting simulation...")
    println("-" ^ 40)

    elapsed = @elapsed begin
        Wflow.run(config_path)
    end

    println("-" ^ 40)
    @printf("Simulation completed in %.2f seconds\n", elapsed)
    println()

    # Output summary
    run_dir = joinpath(dirname(config_path), "run_default")
    output_nc = joinpath(run_dir, "output.nc")
    output_csv = joinpath(run_dir, "output.csv")

    println("Output files:")
    if isfile(output_nc)
        size_mb = filesize(output_nc) / 1024 / 1024
        @printf("  - output.nc: %.2f MB\n", size_mb)
    end
    if isfile(output_csv)
        println("  - output.csv: Discharge time series")
    end

    println()
    println("Simulation complete.")
end

main()

