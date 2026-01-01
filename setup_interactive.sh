#!/bin/bash
################################################################################
# FWG LLM Training - Interactive Learning Setup Script
# Automatically sets up the complete interactive learning environment
################################################################################

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🏛️  FWG LLM AGENTIC TRAINING - INTERACTIVE SETUP                          ║
║                                                                              ║
║   Setting up your complete interactive learning environment...              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Function to print status messages
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if running from correct directory
if [ ! -f "README.md" ] || [ ! -d "interactive" ]; then
    print_error "Please run this script from the repository root directory"
    exit 1
fi

print_status "Found repository root directory"

# Step 1: Check Python version
echo -e "\n${BLUE}[1/7] Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python 3 detected: $PYTHON_VERSION"

    # Check if version is 3.11+
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 11 ]; then
        print_status "Python version is compatible (3.11+)"
    else
        print_warning "Python 3.11+ recommended (you have $PYTHON_VERSION)"
        print_info "Interactive features will still work, but some features may be limited"
    fi
else
    print_error "Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Step 2: Create virtual environment
echo -e "\n${BLUE}[2/7] Setting up Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created: venv/"
else
    print_warning "Virtual environment already exists, skipping creation"
fi

# Step 3: Activate virtual environment
echo -e "\n${BLUE}[3/7] Activating virtual environment...${NC}"
source venv/bin/activate
print_status "Virtual environment activated"

# Step 4: Upgrade pip
echo -e "\n${BLUE}[4/7] Upgrading pip...${NC}"
pip install --upgrade pip -q
print_status "pip upgraded to latest version"

# Step 5: Install dependencies
echo -e "\n${BLUE}[5/7] Installing interactive learning dependencies...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}\n"

if pip install -r interactive/requirements.txt; then
    print_status "All dependencies installed successfully"
else
    print_error "Failed to install some dependencies"
    print_info "You can try installing manually with: pip install -r interactive/requirements.txt"
    exit 1
fi

# Step 6: Check optional dependencies
echo -e "\n${BLUE}[6/7] Checking optional dependencies...${NC}"

# Check Ollama
if command -v ollama &> /dev/null; then
    print_status "Ollama detected (for local LLM exercises)"

    # Check if Ollama is running
    if ollama list &> /dev/null; then
        print_status "Ollama service is running"
        MODEL_COUNT=$(ollama list | wc -l)
        print_info "Models available: $((MODEL_COUNT - 1))"
    else
        print_warning "Ollama is installed but not running"
        print_info "Start it with: ollama serve"
    fi
else
    print_warning "Ollama not found (optional, but recommended for Module 03)"
    print_info "Install from: https://ollama.ai"
fi

# Check Node.js (for some advanced exercises)
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js detected: $NODE_VERSION (for MCP exercises)"
else
    print_warning "Node.js not found (optional, needed for Module 06 MCP exercises)"
    print_info "Install from: https://nodejs.org"
fi

# Step 7: Initialize progress tracking
echo -e "\n${BLUE}[7/7] Initializing progress tracking system...${NC}"

cd interactive/progress-tracking
if python3 -c "from tracker import ProgressTracker; tracker = ProgressTracker(); print('✅ Success')" &> /dev/null; then
    print_status "Progress tracking database initialized"
else
    print_warning "Progress tracking setup encountered an issue"
    print_info "You can still use the system, progress just won't be saved"
fi
cd ../..

# Final summary
echo -e "\n${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ✅ SETUP COMPLETE!                                                         ║
║                                                                              ║
║   Your interactive learning environment is ready to use.                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

print_info "Quick Start Commands:\n"

echo -e "  ${BLUE}Start a quiz:${NC}"
echo -e "    python interactive/quizzes/quiz_module01.py\n"

echo -e "  ${BLUE}Begin Lab 00:${NC}"
echo -e "    cd interactive/labs/lab00_hello_agent\n"

echo -e "  ${BLUE}Check your progress:${NC}"
echo -e "    python interactive/progress-tracking/tracker.py dashboard\n"

echo -e "  ${BLUE}View interactive hub:${NC}"
echo -e "    cat interactive/README.md\n"

echo -e "  ${BLUE}Launch web dashboard (coming soon):${NC}"
echo -e "    python interactive/dashboard.py\n"

print_warning "Remember to activate the virtual environment before each session:"
echo -e "    ${BLUE}source venv/bin/activate${NC}\n"

print_status "Happy learning! 🎓"
echo ""
