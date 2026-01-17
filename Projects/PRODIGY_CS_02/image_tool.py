#!/usr/bin/env python3
"""
Image Encryption Tool
Developed by Ben De Silver
Cross-platform image encryption/decryption using XOR cipher
"""

import os
import sys
import argparse
from pathlib import Path

# Platform-independent imports
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class ImageEncryptionTool:
    def __init__(self):
        self.tool_name = "Image Encryption Tool"
        self.developer = "Ben De Silver"
        self.width = 60
    
    def clear_screen(self):
        """Clear screen in a cross-platform way"""
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # macOS and Linux
            os.system('clear')
    
    def display_banner(self):
        """Display clean, cross-platform banner"""
        self.clear_screen()
        border = "=" * self.width
        print(f"\n{border}")
        print("IMAGE ENCRYPTION TOOL".center(self.width))
        print("Developed by Ben De Silver".center(self.width))
        print(border)
    
    def display_menu(self):
        """Display main menu"""
        border = "-" * self.width
        print(f"\n{border}")
        print("MAIN MENU".center(self.width))
        print(border)
        print()
        print(" " * 20 + "[1] Encrypt Image")
        print(" " * 20 + "[2] Decrypt Image")
        print(" " * 20 + "[3] About & Help")
        print(" " * 20 + "[4] Check Dependencies")
        print(" " * 20 + "[5] Exit")
        print()
        print(border)
    
    def get_user_input(self, prompt, password=False):
        """Get user input in a cross-platform way"""
        if password:
            try:
                import getpass
                return getpass.getpass(prompt)
            except (ImportError, Exception):
                # Fallback for systems without getpass
                print("WARNING: Password will be visible")
                return input(prompt)
        return input(prompt)
    
    def check_dependencies(self):
        """Check if required packages are installed"""
        print("\n" + "-" * self.width)
        print("DEPENDENCY CHECK".center(self.width))
        print("-" * self.width)
        
        if PIL_AVAILABLE:
            print(f"\n[✓] Pillow library is installed")
            print(f"    Version: {Image.__version__}")
        else:
            print("\n[✗] Pillow library is NOT installed")
            print("\nInstallation instructions:")
            print("\n  On Windows:")
            print("    pip install pillow")
            print("    or: python -m pip install pillow")
            
            print("\n  On macOS/Linux:")
            print("    pip3 install pillow")
            print("    or: python3 -m pip install pillow")
            
            print("\n  Using system package manager:")
            print("    Ubuntu/Debian: sudo apt-get install python3-pil")
            print("    Fedora/RHEL: sudo dnf install python3-pillow")
            print("    macOS (Homebrew): brew install pillow")
        
        print("\n" + "-" * self.width)
        input("\nPress Enter to continue...")
        return PIL_AVAILABLE
    
    def get_encryption_key(self, operation="encrypt"):
        """Get encryption/decryption key from user"""
        print("\n" + "-" * self.width)
        print(f"KEY ENTRY - {operation.upper()}".center(self.width))
        print("-" * self.width)
        
        if operation == "encrypt":
            print("\nIMPORTANT:")
            print("• Use a strong key (8+ characters)")
            print("• Save this key securely")
            print("• You'll need it to decrypt the image")
            print("\n" + "-" * self.width)
            
            while True:
                key = self.get_user_input("\nEnter encryption key: ", password=True)
                
                if not key:
                    print("Key cannot be empty!")
                    continue
                
                if len(key) < 4:
                    print("Warning: Key is very short (minimum 4 characters recommended)")
                    proceed = self.get_user_input("Continue anyway? (y/n): ").lower()
                    if proceed not in ['y', 'yes']:
                        continue
                
                confirm = self.get_user_input("Confirm encryption key: ", password=True)
                
                if key == confirm:
                    return key
                else:
                    print("Keys don't match! Please try again.")
        else:
            print("\nEnter the encryption key used for this image:")
            key = self.get_user_input("\nEnter decryption key: ", password=True)
            return key
    
    def process_image(self, input_path, output_path, key, operation):
        """Process image for encryption or decryption"""
        if not PIL_AVAILABLE:
            print("\n[!] Error: Pillow library not found.")
            print("    Please run 'Check Dependencies' first.")
            return False
        
        try:
            # Validate input file
            if not os.path.exists(input_path):
                print(f"\n[!] Error: File not found: {input_path}")
                return False
            
            # Create output directory if needed
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            print("\n" + "-" * self.width)
            print(f"PROCESSING IMAGE".center(self.width))
            print("-" * self.width)
            print(f"\nOperation: {operation}")
            print(f"Input: {os.path.basename(input_path)}")
            print(f"Output: {os.path.basename(output_path)}")
            print(f"Key length: {len(key)} characters")
            
            # Open and process the image
            with Image.open(input_path) as img:
                # Convert image to appropriate mode
                if img.mode == 'P':
                    img = img.convert('RGBA')
                elif img.mode not in ['RGB', 'RGBA', 'L']:
                    img = img.convert('RGB')
                
                pixels = img.load()
                width, height = img.size
                
                # Generate seed from key
                seed = sum(ord(c) for c in key) % 256
                
                # Progress tracking
                total_pixels = width * height
                print(f"\nImage size: {width} × {height} ({total_pixels:,} pixels)")
                print("\nProcessing: [", end="")
                
                # Process each pixel
                for y in range(height):
                    for x in range(width):
                        if img.mode == 'RGB':
                            r, g, b = pixels[x, y]
                            pixels[x, y] = (r ^ seed, g ^ seed, b ^ seed)
                        elif img.mode == 'RGBA':
                            r, g, b, a = pixels[x, y]
                            pixels[x, y] = (r ^ seed, g ^ seed, b ^ seed, a)
                        elif img.mode == 'L':
                            pixels[x, y] = pixels[x, y] ^ seed
                    
                    # Update progress bar
                    if y % (height // 20) == 0:
                        print("█", end="", flush=True)
                
                print("] 100%")
                
                # Save the processed image
                img.save(output_path, optimize=True)
                
                # Show file information
                input_size = os.path.getsize(input_path)
                output_size = os.path.getsize(output_path)
                
                print("\n" + "-" * self.width)
                print("COMPLETED SUCCESSFULLY".center(self.width))
                print("-" * self.width)
                print(f"\n✓ {operation.capitalize()}ion complete!")
                print(f"   Original size: {self.format_file_size(input_size)}")
                print(f"   Processed size: {self.format_file_size(output_size)}")
                print(f"   Saved to: {output_path}")
                
                return True
                
        except Exception as e:
            print(f"\n[!] Error during {operation}: {str(e)}")
            return False
    
    def format_file_size(self, bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"
    
    def select_file_interactive(self):
        """Interactive file selection"""
        print("\n" + "-" * self.width)
        print("FILE SELECTION".center(self.width))
        print("-" * self.width)
        
        print("\nOptions:")
        print("  1. Enter file path manually")
        print("  2. Browse current directory")
        print("  3. Return to main menu")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '3':
            return None
        
        if choice == '2':
            # List files in current directory
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif']
            image_files = [f for f in files if any(f.lower().endswith(ext) for ext in image_extensions)]
            
            if not image_files:
                print("\nNo image files found in current directory.")
                return None
            
            print("\nAvailable image files:")
            for i, file in enumerate(image_files[:20], 1):
                print(f"  {i}. {file}")
            
            try:
                selection = int(input(f"\nSelect file (1-{len(image_files)}): "))
                if 1 <= selection <= len(image_files):
                    return image_files[selection - 1]
            except (ValueError, IndexError):
                print("Invalid selection.")
                return None
        
        # Manual path entry
        while True:
            path = input("\nEnter file path: ").strip()
            if not path:
                print("Path cannot be empty.")
                continue
            
            if not os.path.exists(path):
                print(f"File not found: {path}")
                print("Try again or press Enter to cancel.")
                if not input("Press Enter to cancel, or type 'retry' to try again: ").strip():
                    return None
                continue
            
            return path
    
    def encrypt_image(self):
        """Encrypt an image"""
        self.clear_screen()
        print("\n" + "=" * self.width)
        print("ENCRYPT IMAGE".center(self.width))
        print("=" * self.width)
        
        # Select input file
        print("\nSelect an image to encrypt:")
        input_path = self.select_file_interactive()
        if input_path is None:
            return
        
        # Get output file name
        print(f"\nSelected: {input_path}")
        default_name = f"encrypted_{os.path.splitext(os.path.basename(input_path))[0]}.png"
        output_path = input(f"\nOutput file name [default: {default_name}]: ").strip()
        if not output_path:
            output_path = default_name
        
        # Get encryption key
        key = self.get_encryption_key("encrypt")
        if not key:
            print("\n[!] No key provided. Operation cancelled.")
            return
        
        # Process the image
        if self.process_image(input_path, output_path, key, "encrypt"):
            print("\n" + "=" * self.width)
            print("IMPORTANT REMINDER".center(self.width))
            print("=" * self.width)
            print("\n✓ Save your encryption key:")
            print(f"   Key: {'*' * len(key)}")
            print(f"   (Length: {len(key)} characters)")
            print("\nWithout this key, you CANNOT decrypt the image!")
        
        input("\nPress Enter to continue...")
    
    def decrypt_image(self):
        """Decrypt an image"""
        self.clear_screen()
        print("\n" + "=" * self.width)
        print("DECRYPT IMAGE".center(self.width))
        print("=" * self.width)
        
        # Select input file
        print("\nSelect an encrypted image to decrypt:")
        input_path = self.select_file_interactive()
        if input_path is None:
            return
        
        # Get output file name
        print(f"\nSelected: {input_path}")
        default_name = f"decrypted_{os.path.splitext(os.path.basename(input_path))[0]}.png"
        output_path = input(f"\nOutput file name [default: {default_name}]: ").strip()
        if not output_path:
            output_path = default_name
        
        # Get decryption key
        key = self.get_encryption_key("decrypt")
        if not key:
            print("\n[!] No key provided. Operation cancelled.")
            return
        
        # Process the image
        if self.process_image(input_path, output_path, key, "decrypt"):
            print("\n✓ Image successfully decrypted!")
            print(f"   Saved to: {output_path}")
        
        input("\nPress Enter to continue...")
    
    def show_about(self):
        """Display about information"""
        self.clear_screen()
        print("\n" + "=" * self.width)
        print("ABOUT & HELP".center(self.width))
        print("=" * self.width)
        
        about_text = f"""
        {self.tool_name}
        Developed by: {self.developer}
        
        DESCRIPTION
        -----------
        A cross-platform tool for encrypting and decrypting images
        using XOR cipher. The tool converts your password into a
        numeric seed and applies XOR operation to each pixel.
        
        FEATURES
        --------
        • XOR-based encryption/decryption
        • Cross-platform (Windows, macOS, Linux)
        • Multiple image format support
        • Interactive and command-line modes
        • Progress visualization
        • Secure key handling
        
        SECURITY NOTES
        --------------
        • XOR encryption is symmetric (same key encrypts/decrypts)
        • The key is converted to a 0-255 numeric seed
        • Keep your encryption key secure and private
        • This method provides basic security for casual use
        
        SUPPORTED FORMATS
        -----------------
        • PNG, JPEG/JPG, BMP, GIF, TIFF
        
        USAGE
        -----
        1. Select 'Encrypt Image' from the menu
        2. Choose an image file
        3. Create and confirm a strong password
        4. Save the encrypted image and your password
        
        To decrypt:
        1. Select 'Decrypt Image'
        2. Choose the encrypted image
        3. Enter the same password
        4. Save the decrypted image
        
        COMMAND LINE USAGE
        ------------------
        python image_tool.py --encrypt input.jpg output.png --key password
        python image_tool.py --decrypt encrypted.png output.jpg --key password
        python image_tool.py --check-deps
        
        TROUBLESHOOTING
        ---------------
        • If images appear corrupted: Wrong password or damaged file
        • If tool doesn't start: Install Pillow: pip install pillow
        • If file not found: Use full path or move to same directory
        
        For issues or questions, contact the developer.
        """
        
        print(about_text)
        print("=" * self.width)
        input("\nPress Enter to return to menu...")
    
    def run_interactive(self):
        """Run in interactive menu mode"""
        while True:
            self.display_banner()
            self.display_menu()
            
            try:
                choice = input("\nSelect an option (1-5): ").strip()
                
                if choice == '1':
                    self.encrypt_image()
                elif choice == '2':
                    self.decrypt_image()
                elif choice == '3':
                    self.show_about()
                elif choice == '4':
                    self.check_dependencies()
                elif choice == '5':
                    print("\n" + "=" * self.width)
                    print("Thank you for using Image Encryption Tool!".center(self.width))
                    print("=" * self.width)
                    print("\nExiting... Goodbye!\n")
                    break
                else:
                    print("\n[!] Invalid option. Please enter 1-5.")
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n[!] Operation cancelled by user.")
                break
            except Exception as e:
                print(f"\n[!] An error occurred: {str(e)}")
                input("\nPress Enter to continue...")
    
    def run_cli(self, args):
        """Run in command-line interface mode"""
        if not PIL_AVAILABLE:
            print("[!] Error: Pillow library is not installed.")
            print("    Install it using: pip install pillow")
            print("    Or run: python image_tool.py and select 'Check Dependencies'")
            sys.exit(1)
        
        if args.operation == 'encrypt':
            if not args.input or not args.output:
                print("[!] Error: Both input and output paths are required for encryption.")
                sys.exit(1)
            
            key = args.key
            if not key:
                key = self.get_user_input("Enter encryption key: ", password=True)
            
            success = self.process_image(args.input, args.output, key, "encrypt")
            if success:
                print(f"\n✓ Encryption complete! File saved to: {args.output}")
            else:
                print("\n[!] Encryption failed.")
                sys.exit(1)
                
        elif args.operation == 'decrypt':
            if not args.input or not args.output:
                print("[!] Error: Both input and output paths are required for decryption.")
                sys.exit(1)
            
            key = args.key
            if not key:
                key = self.get_user_input("Enter decryption key: ", password=True)
            
            success = self.process_image(args.input, args.output, key, "decrypt")
            if success:
                print(f"\n✓ Decryption complete! File saved to: {args.output}")
            else:
                print("\n[!] Decryption failed. Check your key and input file.")
                sys.exit(1)
                
        elif args.operation == 'check':
            self.check_dependencies()

def main():
    """Main entry point"""
    tool = ImageEncryptionTool()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description=f"{tool.tool_name} - Developed by {tool.developer}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encrypt an image:
    %(prog)s --encrypt photo.jpg secret.png --key mypassword
  
  Decrypt an image:
    %(prog)s --decrypt secret.png original.jpg --key mypassword
  
  Check dependencies:
    %(prog)s --check-deps
  
  Interactive mode (default):
    %(prog)s

Supported formats: PNG, JPEG, BMP, GIF, TIFF
        """
    )
    
    # Add arguments
    parser.add_argument('--encrypt', nargs=2, metavar=('INPUT', 'OUTPUT'),
                       help='Encrypt an image')
    parser.add_argument('--decrypt', nargs=2, metavar=('INPUT', 'OUTPUT'),
                       help='Decrypt an image')
    parser.add_argument('--key', '-k', help='Encryption/decryption key')
    parser.add_argument('--check-deps', action='store_true',
                       help='Check dependencies and exit')
    
    args = parser.parse_args()
    
    # Determine operation mode
    if args.encrypt:
        args.operation = 'encrypt'
        args.input, args.output = args.encrypt
        tool.run_cli(args)
    elif args.decrypt:
        args.operation = 'decrypt'
        args.input, args.output = args.decrypt
        tool.run_cli(args)
    elif args.check_deps:
        args.operation = 'check'
        tool.run_cli(args)
    else:
        # No arguments, run interactive mode
        tool.run_interactive()

if __name__ == '__main__':
    main()
