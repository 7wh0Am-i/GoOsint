#!/bin/bash

# GoOsint Installation Script
# This script sets up GoOsint and its dependencies
# Compatible with Linux, macOS, and Termux (Android)

echo "🚀 GoOsint Installation Script"
echo "=============================="

# Detect environment
detect_environment() {
    if [[ -n "$TERMUX_VERSION" ]] || [[ "$PREFIX" == *"com.termux"* ]]; then
        echo "🤖 Termux environment detected"
        return 0  # Termux
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "🐧 Linux environment detected"
        return 1  # Linux
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🍎 macOS environment detected"
        return 2  # macOS
    else
        echo "❓ Unknown environment: $OSTYPE"
        return 3  # Unknown
    fi
}

# Get environment type
detect_environment
ENV_TYPE=$?

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    
    if [[ $ENV_TYPE -eq 0 ]]; then
        echo "📦 Installing Python 3 on Termux..."
        pkg update && pkg install python -y
        if ! command -v python3 &> /dev/null; then
            echo "❌ Failed to install Python 3 on Termux"
            exit 1
        fi
    else
        echo "Please install Python 3.7 or higher manually."
        exit 1
    fi
fi

echo "✅ Python 3 found"

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "📋 Python version: $python_version"

# Install pip if not available
install_pip() {
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        echo "📦 Installing pip..."
        
        case $ENV_TYPE in
            0) # Termux
                pkg install python-pip -y
                ;;
            1) # Linux
                if command -v apt-get &> /dev/null; then
                    sudo apt-get update
                    sudo apt-get install python3-pip -y
                elif command -v yum &> /dev/null; then
                    sudo yum install python3-pip -y
                elif command -v pacman &> /dev/null; then
                    sudo pacman -S python-pip --noconfirm
                else
                    echo "❌ Unable to install pip automatically. Please install manually."
                    exit 1
                fi
                ;;
            2) # macOS
                if command -v brew &> /dev/null; then
                    brew install python3
                else
                    echo "❌ Please install pip manually or install Homebrew first."
                    exit 1
                fi
                ;;
            *) # Unknown
                echo "❌ Unable to install pip automatically. Please install manually."
                exit 1
                ;;
        esac
    fi
}

install_pip

# Install requirements
echo "📦 Installing Python dependencies..."

# Determine the correct pip command
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "❌ pip not found after installation attempt"
    exit 1
fi

# Install dependencies with appropriate method
case $ENV_TYPE in
    0) # Termux
        echo "🤖 Installing dependencies for Termux..."
        $PIP_CMD install --upgrade pip
        $PIP_CMD install -r requirements.txt
        ;;
    1|2|*) # Linux, macOS, or others
        echo "💻 Installing dependencies..."
        $PIP_CMD install --user -r requirements.txt
        ;;
esac

# Make the script executable
chmod +x GoOsint.py

echo ""
echo "✅ Installation complete!"
echo ""
echo "🔧 Next steps:"
echo "1. Set up GHunt authentication:"
if [[ $ENV_TYPE -eq 0 ]]; then
    echo "   python GoOsint.py --setup"
else
    echo "   python3 GoOsint.py --setup"
fi
echo ""
echo "2. Test with a single email:"
if [[ $ENV_TYPE -eq 0 ]]; then
    echo "   python GoOsint.py -e target@gmail.com"
else
    echo "   python3 GoOsint.py -e target@gmail.com"
fi
echo ""
echo "3. For help:"
if [[ $ENV_TYPE -eq 0 ]]; then
    echo "   python GoOsint.py --help"
else
    echo "   python3 GoOsint.py --help"
fi
echo ""

# Termux-specific additional instructions
if [[ $ENV_TYPE -eq 0 ]]; then
    echo "📱 Termux-specific notes:"
    echo "• Make sure to grant storage permissions:"
    echo "  termux-setup-storage"
    echo "• You may need to install additional packages:"
    echo "  pkg install git curl wget"
    echo ""
fi

echo "⚠️  Remember: Use this tool responsibly and only for legal OSINT purposes!"
