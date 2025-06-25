#!/usr/bin/env python3
"""
GoOsint - Gmail OSINT Tool powered by GHunt
A comprehensive Gmail reconnaissance tool for OSINT investigations
"""

import argparse
import sys
import os
import json
import subprocess
from colorama import Fore, Back, Style, init
from datetime import datetime

# Try to import GHunt's globals for rich console, fallback to basic implementation
try:
    from ghunt import globals as gb
    GHUNT_AVAILABLE = True
except ImportError:
    GHUNT_AVAILABLE = False

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class RGBColors:
    """Custom RGB color class using ANSI escape codes"""
    @staticmethod
    def rgb(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
    
    @staticmethod
    def reset():
        return "\033[0m"
    
    # Google brand colors
    GOOGLE_BLUE = rgb.__func__(66, 133, 244)      # #4285F4
    GOOGLE_RED = rgb.__func__(234, 67, 53)        # #EA4335
    GOOGLE_YELLOW = rgb.__func__(251, 188, 4)     # #FBBC04
    GOOGLE_GREEN = rgb.__func__(52, 168, 83)      # #34A853
    WHITE = rgb.__func__(255, 255, 255)           # #FFFFFF
    LIGHT_BLUE = rgb.__func__(138, 180, 248)      # #8AB4F8

def show_banner():
    """Show GoOsint banner in GHunt style"""
    if GHUNT_AVAILABLE:
        banner = """
    [blue] ██████╗  ██████╗ [/][blue] ██████╗ ███████╗██╗███╗   ██╗████████╗[/]
    [blue]██╔════╝ ██╔═══██╗[/][blue]██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝[/]
    [blue]██║  ███╗██║   ██║[/][blue]██║   ██║███████╗██║██╔██╗ ██║   ██║   [/]
    [blue]██║   ██║██║   ██║[/][blue]██║   ██║╚════██║██║██║╚██╗██║   ██║   [/]
    [blue]╚██████╔╝╚██████╔╝[/][blue]╚██████╔╝███████║██║██║ ╚████║   ██║   [/]
    [blue] ╚═════╝  ╚═════╝ [/][blue]╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   [/]

             [bold][blue]Gmail OSINT Tool powered by GHunt[/blue][/bold]
             [cyan]Version 1.0 | Author: OSINT Researcher[/cyan]
        [yellow]⚠️  For Educational and Legal OSINT purposes only ⚠️[/yellow]
        """
        try:
            gb.rc.print(banner)
        except Exception:
            # Fallback to basic print
            print("GoOsint - Gmail OSINT Tool powered by GHunt")
    else:
        print("GoOsint - Gmail OSINT Tool powered by GHunt")

class GoOsint:
    def __init__(self):
        # Rich console banner in GHunt style
        self.rich_banner = """
    [blue] ██████╗  ██████╗ [/][blue] ██████╗ ███████╗██╗███╗   ██╗████████╗[/]
    [blue]██╔════╝ ██╔═══██╗[/][blue]██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝[/]
    [blue]██║  ███╗██║   ██║[/][blue]██║   ██║███████╗██║██╔██╗ ██║   ██║   [/]
    [blue]██║   ██║██║   ██║[/][blue]██║   ██║╚════██║██║██║╚██╗██║   ██║   [/]
    [blue]╚██████╔╝╚██████╔╝[/][blue]╚██████╔╝███████║██║██║ ╚████║   ██║   [/]
    [blue] ╚═════╝  ╚═════╝ [/][blue]╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   [/]

             [bold][blue]Gmail OSINT Tool powered by GHunt[/blue][/bold]
             [cyan]Version 1.0 | Author: 7wh0Am-i[/cyan]
        [yellow]⚠️  For Educational and Legal OSINT purposes only ⚠️[/yellow]
    """
        
        # Fallback banner for when GHunt is not available
        self.fallback_banner = f"""
{RGBColors.GOOGLE_BLUE}
 ██████╗  ██████╗ {RGBColors.GOOGLE_BLUE}██████╗ ███████╗██╗███╗   ██╗████████╗
{RGBColors.GOOGLE_BLUE}██╔════╝ ██╔═══██╗{RGBColors.GOOGLE_BLUE}██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
{RGBColors.GOOGLE_BLUE}██║  ███╗██║   ██║{RGBColors.GOOGLE_BLUE}██║   ██║███████╗██║██╔██╗ ██║   ██║   
{RGBColors.GOOGLE_BLUE}██║   ██║██║   ██║{RGBColors.GOOGLE_BLUE}██║   ██║╚════██║██║██║╚██╗██║   ██║   
{RGBColors.GOOGLE_BLUE}╚██████╔╝╚██████╔╝{RGBColors.GOOGLE_BLUE}╚██████╔╝███████║██║██║ ╚████║   ██║   
{RGBColors.GOOGLE_BLUE} ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
{RGBColors.reset()}
{RGBColors.GOOGLE_BLUE}        Gmail OSINT Tool powered by GHunt{RGBColors.reset()}
{RGBColors.LIGHT_BLUE}        Version 1.0 | Author: 7wh0Am-i{RGBColors.reset()}
{RGBColors.WHITE}        ⚠️  For Educational and Legal OSINT purposes only ⚠️{RGBColors.reset()}
{RGBColors.GOOGLE_BLUE}═══════════════════════════════════════════════════════════{RGBColors.reset()}
"""
        # Initialize results storage
        self.results_folder = "results"
        self.ensure_results_folder()
        self.results_file = os.path.join(self.results_folder, f"investigation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        self.all_results = {
            "session_info": {
                "start_time": datetime.now().isoformat(),
                "tool_version": "1.0",
                "total_investigations": 0
            },
            "investigations": []
        }

    def ensure_results_folder(self):
        """Create results folder if it doesn't exist"""
        try:
            if not os.path.exists(self.results_folder):
                os.makedirs(self.results_folder)
                print(f"{RGBColors.GOOGLE_GREEN}✓ Created results folder: {self.results_folder}{RGBColors.reset()}")
        except Exception as e:
            print(f"{RGBColors.GOOGLE_RED}✗ Error creating results folder: {str(e)}{RGBColors.reset()}")
            # Fallback to current directory
            self.results_folder = "."

    def print_banner(self):
        """Display the GoOsint banner using GHunt's rich console if available"""
        if GHUNT_AVAILABLE:
            try:
                gb.rc.print(self.rich_banner)
            except Exception:
                # If rich console fails, fallback to regular banner
                print(self.fallback_banner)
        else:
            print(self.fallback_banner)

    def parse_ghunt_output(self, output_lines, email):
        """Parse GHunt output into structured JSON data"""
        investigation_data = {
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "google_account": {},
            "services": {},
            "profile": {},
            "raw_output": output_lines
        }
        
        current_section = None
        
        for line in output_lines:
            line = line.strip()
            if not line:
                continue
                
            # Parse different sections
            if "🙋 Google Account data" in line:
                current_section = "google_account"
            elif "📞 Google Chat Extended Data" in line:
                current_section = "google_chat"
            elif "🌐 Google Plus Extended Data" in line:
                current_section = "google_plus"
            elif "🎮 Play Games data" in line:
                current_section = "play_games"
            elif "🗺️ Maps data" in line:
                current_section = "maps"
            elif "🗓️ Calendar data" in line:
                current_section = "calendar"
            elif "🎵 YouTube data" in line:
                current_section = "youtube"
            
            # Extract specific information
            if "Email :" in line:
                investigation_data["profile"]["email"] = line.split("Email :")[1].strip()
            elif "Gaia ID :" in line:
                investigation_data["profile"]["gaia_id"] = line.split("Gaia ID :")[1].strip()
            elif "Last profile edit :" in line:
                investigation_data["profile"]["last_edit"] = line.split("Last profile edit :")[1].strip()
            elif line.startswith("=> https://"):
                if "profile" not in investigation_data["profile"]:
                    investigation_data["profile"]["profile_picture"] = line.replace("=> ", "")
            elif "Profile page :" in line:
                investigation_data["services"]["maps_profile"] = line.split("Profile page :")[1].strip()
            elif "Entity Type :" in line:
                investigation_data["services"]["chat_entity_type"] = line.split("Entity Type :")[1].strip()
            elif "Customer ID :" in line:
                investigation_data["services"]["chat_customer_id"] = line.split("Customer ID :")[1].strip()
            elif "Entreprise User :" in line:
                investigation_data["services"]["enterprise_user"] = line.split("Entreprise User :")[1].strip()
            elif line.startswith("[+]") and "Activated Google services" in line:
                investigation_data["services"]["activated_services"] = []
            elif line.startswith("- ") and current_section in ["google_plus"]:
                if "activated_services" not in investigation_data["services"]:
                    investigation_data["services"]["activated_services"] = []
                investigation_data["services"]["activated_services"].append(line[2:])
            elif "Reviews :" in line:
                investigation_data["services"]["maps_reviews"] = line.split("Reviews :")[1].strip()
            elif "Photos :" in line:
                investigation_data["services"]["maps_photos"] = line.split("Photos :")[1].strip()
            elif "Answers :" in line:
                investigation_data["services"]["maps_answers"] = line.split("Answers :")[1].strip()
                
        return investigation_data

    def save_results_to_json(self):
        """Save all results to a single JSON file"""
        try:
            self.all_results["session_info"]["end_time"] = datetime.now().isoformat()
            self.all_results["session_info"]["total_investigations"] = len(self.all_results["investigations"])
            
            with open(self.results_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_results, f, indent=2, ensure_ascii=False)
            
            # Show relative path for cleaner output
            relative_path = os.path.relpath(self.results_file)
            print(f"{RGBColors.GOOGLE_GREEN}✓ All results saved to: {relative_path}{RGBColors.reset()}")
            return True
        except Exception as e:
            print(f"{RGBColors.GOOGLE_RED}✗ Error saving results: {str(e)}{RGBColors.reset()}")
            return False

    def check_ghunt_installation(self):
        """Check if GHunt is installed and available"""
        try:
            # Check if ghunt command exists without showing banner
            result = subprocess.run(['which', 'ghunt'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"{RGBColors.GOOGLE_GREEN}✓ GHunt is installed and ready{RGBColors.reset()}")
                return True
            else:
                print(f"{RGBColors.GOOGLE_RED}✗ GHunt not found{RGBColors.reset()}")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"{RGBColors.GOOGLE_RED}✗ GHunt is not installed{RGBColors.reset()}")
            return False

    def install_ghunt(self):
        """Install GHunt using pip"""
        print(f"{RGBColors.GOOGLE_YELLOW}Installing GHunt...{RGBColors.reset()}")
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'ghunt'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{RGBColors.GOOGLE_GREEN}✓ GHunt installed successfully{RGBColors.reset()}")
                return True
            else:
                print(f"{RGBColors.GOOGLE_RED}✗ Failed to install GHunt: {result.stderr}{RGBColors.reset()}")
                return False
        except Exception as e:
            print(f"{RGBColors.GOOGLE_RED}✗ Error installing GHunt: {str(e)}{RGBColors.reset()}")
            return False

    def email_investigation(self, email):
        """Perform email investigation using GHunt"""
        print(f"\n{RGBColors.LIGHT_BLUE}🔍 Investigating email: {email}{RGBColors.reset()}")
        print(f"{RGBColors.GOOGLE_YELLOW}{'='*60}{RGBColors.reset()}")
        
        try:
            # Run GHunt email investigation with output capture to hide banner
            result = subprocess.run(['ghunt', 'email', email], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Filter out the GHunt banner and keep only the investigation results
                output_lines = result.stdout.split('\n')
                filtered_output = []
                skip_banner = True
                
                for line in output_lines:
                    # Skip lines until we find actual investigation content
                    if skip_banner:
                        if ('Target' in line or 'Name' in line or 'Email' in line or 
                            'Google ID' in line or '[+]' in line or '[-]' in line or
                            'Profile' in line or 'YouTube' in line or 'Photos' in line):
                            skip_banner = False
                            filtered_output.append(line)
                    else:
                        filtered_output.append(line)
                
                # Display filtered results with colors
                if filtered_output:
                    print(f"{RGBColors.GOOGLE_GREEN}Investigation Results:{RGBColors.reset()}")
                    print()  # Add gap after header
                    
                    section_headers = ['🙋', '📞', '🌐', '🎮', '🗺️', '🗓️', '🎵', '📱', '🔍']
                    
                    for line in filtered_output:
                        if line.strip():
                            # Add gap before section headers (emoji-based sections)
                            if any(header in line for header in section_headers):
                                print()  # Gap before new section
                            
                            # Colorize different types of output
                            if line.startswith('[+]'):
                                print(f"{RGBColors.GOOGLE_GREEN}{line}{RGBColors.reset()}")
                            elif line.startswith('[-]'):
                                print(f"{RGBColors.GOOGLE_RED}{line}{RGBColors.reset()}")
                            elif line.startswith('[!]'):
                                print(f"{RGBColors.GOOGLE_YELLOW}{line}{RGBColors.reset()}")
                            elif 'Name:' in line or 'Email:' in line or 'Google ID:' in line:
                                print(f"{RGBColors.LIGHT_BLUE}{line}{RGBColors.reset()}")
                            elif any(header in line for header in section_headers):
                                print(f"{RGBColors.GOOGLE_BLUE}{line}{RGBColors.reset()}")  # Section headers in blue
                            else:
                                print(line)
                            
                            # Add gap after certain result types for better readability
                            if (line.startswith('=>') or 
                                'Profile page :' in line or 
                                'Last profile edit :' in line or
                                'User types :' in line):
                                print()  # Gap after important info
                    
                    # Parse and store results in JSON format
                    investigation_data = self.parse_ghunt_output(filtered_output, email)
                    self.all_results["investigations"].append(investigation_data)
                                
                else:
                    print(f"{RGBColors.GOOGLE_YELLOW}No detailed information found for this email{RGBColors.reset()}")
                    # Store failed investigation
                    investigation_data = {
                        "email": email,
                        "timestamp": datetime.now().isoformat(),
                        "status": "no_data",
                        "message": "No detailed information found"
                    }
                    self.all_results["investigations"].append(investigation_data)
                
                print()  # Add gap after results
                
            else:
                # Handle error output with colors
                error_output = result.stderr.strip()
                if error_output:
                    print(f"{RGBColors.GOOGLE_RED}✗ Investigation failed: {error_output}{RGBColors.reset()}")
                else:
                    print(f"{RGBColors.GOOGLE_RED}✗ Investigation failed with no error details{RGBColors.reset()}")
                
                # Store failed investigation in JSON
                investigation_data = {
                    "email": email,
                    "timestamp": datetime.now().isoformat(),
                    "status": "failed",
                    "error": error_output if error_output else "No error details"
                }
                self.all_results["investigations"].append(investigation_data)
                
        except subprocess.TimeoutExpired:
            print(f"{RGBColors.GOOGLE_RED}✗ Investigation timed out{RGBColors.reset()}")
            # Store timeout in JSON
            investigation_data = {
                "email": email,
                "timestamp": datetime.now().isoformat(),
                "status": "timeout",
                "error": "Investigation timed out after 60 seconds"
            }
            self.all_results["investigations"].append(investigation_data)
        except Exception as e:
            print(f"{RGBColors.GOOGLE_RED}✗ Error during investigation: {str(e)}{RGBColors.reset()}")
            # Store exception in JSON
            investigation_data = {
                "email": email,
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
            self.all_results["investigations"].append(investigation_data)

    def batch_investigation(self, email_file):
        """Perform batch investigation from email list file"""
        if not os.path.exists(email_file):
            print(f"{RGBColors.GOOGLE_RED}✗ Email list file not found: {email_file}{RGBColors.reset()}")
            return
        
        print(f"\n{RGBColors.LIGHT_BLUE}📋 Starting batch investigation from: {email_file}{RGBColors.reset()}")
        
        try:
            with open(email_file, 'r') as f:
                emails = [line.strip() for line in f if line.strip() and '@' in line]
            
            if not emails:
                print(f"{RGBColors.GOOGLE_RED}✗ No valid emails found in file{RGBColors.reset()}")
                return
            
            print(f"{RGBColors.GOOGLE_GREEN}Found {len(emails)} email(s) to investigate{RGBColors.reset()}")
            
            for i, email in enumerate(emails, 1):
                print(f"\n{RGBColors.GOOGLE_BLUE}[{i}/{len(emails)}] Processing: {email}{RGBColors.reset()}")
                print(f"{RGBColors.GOOGLE_BLUE}{'─' * 60}{RGBColors.reset()}")  # Visual separator
                self.email_investigation(email)
                
                # Add spacing between each email investigation (except for the last one)
                if i < len(emails):
                    print(f"\n{RGBColors.GOOGLE_YELLOW}{'═' * 60}{RGBColors.reset()}")
                    print(f"{RGBColors.GOOGLE_YELLOW}Moving to next email...{RGBColors.reset()}")
                    print(f"{RGBColors.GOOGLE_YELLOW}{'═' * 60}{RGBColors.reset()}\n")
            
            # Save all results to JSON file after batch completion
            print(f"\n{RGBColors.LIGHT_BLUE}📄 Saving batch investigation results...{RGBColors.reset()}")
            self.save_results_to_json()
                
        except Exception as e:
            print(f"{RGBColors.GOOGLE_RED}✗ Error reading email list: {str(e)}{RGBColors.reset()}")

    def setup_ghunt(self):
        """Setup GHunt authentication"""
        print(f"\n{RGBColors.LIGHT_BLUE}⚙️  Setting up GHunt authentication...{RGBColors.reset()}")
        print(f"{RGBColors.GOOGLE_YELLOW}This will guide you through the GHunt setup process{RGBColors.reset()}")
        
        try:
            # Run GHunt login to setup authentication (banner will show during interactive setup)
            subprocess.run(['ghunt', 'login'], timeout=300)
            print(f"{RGBColors.GOOGLE_GREEN}✓ GHunt authentication setup completed{RGBColors.reset()}")
        except subprocess.TimeoutExpired:
            print(f"{RGBColors.GOOGLE_RED}✗ Setup process timed out{RGBColors.reset()}")
        except Exception as e:
            print(f"{RGBColors.GOOGLE_RED}✗ Error during setup: {str(e)}{RGBColors.reset()}")

    def show_help(self):
        """Display help information"""
        help_text = f"""
{RGBColors.LIGHT_BLUE}GoOsint Help{RGBColors.reset()}
{RGBColors.GOOGLE_YELLOW}{'='*50}{RGBColors.reset()}

{RGBColors.GOOGLE_GREEN}Commands:{RGBColors.reset()}
  -e, --email EMAIL     Investigate a single email address
  -f, --file FILE       Batch investigate emails from file
  -s, --setup          Setup GHunt authentication
  -i, --install        Install/reinstall GHunt
  -h, --help           Show this help message

{RGBColors.GOOGLE_GREEN}Examples:{RGBColors.reset()}
  python3 goosint.py -e target@gmail.com
  python3 goosint.py -f email_list.txt
  python3 goosint.py --setup

{RGBColors.GOOGLE_GREEN}Email List Format:{RGBColors.reset()}
  Create a text file with one email per line:
  target1@gmail.com
  target2@gmail.com
  target3@gmail.com

{RGBColors.GOOGLE_GREEN}Output:{RGBColors.reset()}
  Results are saved in JSON format to: results/
  Each investigation session creates a timestamped file.

{RGBColors.GOOGLE_RED}Legal Notice:{RGBColors.reset()}
  This tool is for educational and legal OSINT purposes only.
  Always ensure you have proper authorization before investigating.

{RGBColors.LIGHT_BLUE}{'='*50}{RGBColors.reset()}
"""
        print(help_text)

def main():
    parser = argparse.ArgumentParser(
        description="GoOsint - Gmail OSINT Tool powered by GHunt",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-e', '--email', 
                       help='Email address to investigate')
    parser.add_argument('-f', '--file', 
                       help='File containing list of emails to investigate')
    parser.add_argument('-s', '--setup', action='store_true',
                       help='Setup GHunt authentication')
    parser.add_argument('-i', '--install', action='store_true',
                       help='Install/reinstall GHunt')
    parser.add_argument('--no-banner', action='store_true',
                       help='Skip banner display')
    
    args = parser.parse_args()
    
    # Initialize GoOsint
    goosint = GoOsint()
    
    # Show banner unless disabled
    if not args.no_banner:
        goosint.print_banner()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        goosint.show_help()
        return
    
    # Handle install option
    if args.install:
        goosint.install_ghunt()
        return
    
    # Handle setup option
    if args.setup:
        goosint.setup_ghunt()
        return
    
    # Check if GHunt is installed
    if not goosint.check_ghunt_installation():
        print(f"\n{RGBColors.GOOGLE_YELLOW}GHunt is required but not installed.{RGBColors.reset()}")
        install = input(f"{RGBColors.LIGHT_BLUE}Would you like to install it now? (y/n): {RGBColors.reset()}")
        if install.lower() in ['y', 'yes']:
            if goosint.install_ghunt():
                print(f"{RGBColors.GOOGLE_GREEN}Installation complete! Please run the setup command:{RGBColors.reset()}")
                print(f"{RGBColors.LIGHT_BLUE}python3 GoOsint.py --setup{RGBColors.reset()}")
            return
        else:
            print(f"{RGBColors.GOOGLE_RED}GHunt is required to use GoOsint. Exiting.{RGBColors.reset()}")
            return
    
    # Handle email investigation
    if args.email:
        if '@' not in args.email:
            print(f"{RGBColors.GOOGLE_RED}✗ Invalid email format: {args.email}{RGBColors.reset()}")
            return
        goosint.email_investigation(args.email)
        # Save results to JSON file
        goosint.save_results_to_json()
    
    # Handle batch investigation
    elif args.file:
        goosint.batch_investigation(args.file)
    
    else:
        goosint.show_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RGBColors.GOOGLE_YELLOW}Investigation interrupted by user{RGBColors.reset()}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RGBColors.GOOGLE_RED}Unexpected error: {str(e)}{RGBColors.reset()}")
        sys.exit(1)
