import os

def main():
    directories = [
        "output",
        "fabrication_output",
        "simulation_results",
        "verification_results",
        "logs",
        "pipeline_output"
    ]
    
    print("Setting up BockQSC1090 environment...")
    
    for d in directories:
        os.makedirs(d, exist_ok=True)
        print(f"Ensured directory exists: {d}/")
        
    print("Environment setup complete.")

if __name__ == "__main__":
    main()
