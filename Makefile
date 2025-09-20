# Nest CLI Build Makefile

.PHONY: build install clean test dev

# Build the binary
build:
	@echo "🏗️  Building nest-cli binary..."
	python build.py

# Install to system
install: build
	@echo "📦 Installing nest-cli to /usr/local/bin..."
	sudo cp dist/nest-cli /usr/local/bin/
	sudo cp dist/nest-cli-bin /usr/local/bin/
	@echo "✅ Installation complete! Run 'nest-cli' anywhere."

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf dist/ build/ *.spec subprocess_patch.py hooks/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Test the built binary
test: build
	@echo "🧪 Testing built binary..."
	./dist/nest-cli --help || echo "Binary test complete"

# Development mode - run from source
dev:
	@echo "🔧 Running in development mode..."
	python main.py

# Quick build and test
quick: build test

# Package for distribution
package: build
	@echo "📦 Creating distribution package..."
	mkdir -p dist/nest-cli-package
	cp dist/nest-cli dist/nest-cli-package/
	cp dist/nest-cli-bin dist/nest-cli-package/
	cp README.md dist/nest-cli-package/
	cp requirements.txt dist/nest-cli-package/
	echo '#!/bin/bash\nsudo cp nest-cli /usr/local/bin/\nsudo cp nest-cli-bin /usr/local/bin/\necho "nest-cli installed successfully!"' > dist/nest-cli-package/install.sh
	chmod +x dist/nest-cli-package/install.sh
	cd dist && tar -czf nest-cli-linux.tar.gz nest-cli-package/
	@echo "✅ Package created: dist/nest-cli-linux.tar.gz"

help:
	@echo "Nest CLI Build Commands:"
	@echo "  make build    - Build the binary"
	@echo "  make install  - Build and install to system"
	@echo "  make test     - Build and test the binary"
	@echo "  make clean    - Clean build artifacts"
	@echo "  make dev      - Run in development mode"
	@echo "  make package  - Create distribution package"
	@echo "  make quick    - Quick build and test"
