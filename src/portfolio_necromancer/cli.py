"""Command-line interface for Portfolio Necromancer."""

import argparse
import sys
from pathlib import Path
from .necromancer import PortfolioNecromancer
from .config import Config


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Portfolio Necromancer - Auto-build portfolios from your digital wreckage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate portfolio with default config
  portfolio-necromancer

  # Use custom config file
  portfolio-necromancer --config my-config.yaml

  # Generate with custom output name
  portfolio-necromancer --output my-portfolio

  # Create example config file
  portfolio-necromancer --init

For more information, visit: https://github.com/jmenichole/Portfolio-Necromancer
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Custom name for output portfolio directory'
    )
    
    parser.add_argument(
        '--init',
        action='store_true',
        help='Create example configuration file'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Portfolio Necromancer 0.1.0'
    )
    
    args = parser.parse_args()
    
    # Handle --init flag
    if args.init:
        create_example_config()
        return 0
    
    # Run the necromancer
    try:
        necromancer = PortfolioNecromancer(args.config)
        output_path = necromancer.resurrect(args.output)
        
        if output_path:
            return 0
        else:
            return 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        return 130
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def create_example_config():
    """Create an example configuration file."""
    example_path = Path(__file__).parent.parent.parent / 'config.example.yaml'
    target_path = Path('config.yaml')
    
    if target_path.exists():
        response = input(f"{target_path} already exists. Overwrite? [y/N]: ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    try:
        if example_path.exists():
            import shutil
            shutil.copy(example_path, target_path)
        else:
            # Create minimal config if example doesn't exist
            config = Config()
            config.save(str(target_path))
        
        print(f"✓ Configuration file created: {target_path}")
        print()
        print("Next steps:")
        print("1. Edit config.yaml with your credentials and preferences")
        print("2. Run 'portfolio-necromancer' to generate your portfolio")
        print()
        print("See README.md for detailed configuration instructions.")
    
    except Exception as e:
        print(f"Error creating config file: {e}")


if __name__ == '__main__':
    sys.exit(main())
