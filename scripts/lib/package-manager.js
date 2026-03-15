/**
 * Package manager detection system
 * Intelligently detects and manages npm, pnpm, yarn, bun and other package managers
 *
 * @module package-manager
 */

const fs = require('fs');
const path = require('path');
const { commandExists, readJSON, getProjectRoot, getClaudeConfigDir, isWindows } = require('./utils');

// Package manager configuration
const PACKAGE_MANAGERS = {
  npm: {
    name: 'npm',
    lockFile: 'package-lock.json',
    installCmd: 'npm install',
    runCmd: 'npm run',
    execCmd: 'npx',
    globalFlag: '--global'
  },
  pnpm: {
    name: 'pnpm',
    lockFile: 'pnpm-lock.yaml',
    installCmd: 'pnpm install',
    runCmd: 'pnpm',
    execCmd: 'pnpm dlx',
    globalFlag: '--global'
  },
  yarn: {
    name: 'yarn',
    lockFile: 'yarn.lock',
    installCmd: 'yarn install',
    runCmd: 'yarn',
    execCmd: 'yarn dlx',
    globalFlag: 'global'
  },
  bun: {
    name: 'bun',
    lockFile: 'bun.lockb',
    installCmd: 'bun install',
    runCmd: 'bun run',
    execCmd: 'bun x',
    globalFlag: '--global'
  }
};

// Detection priority
const DETECTION_PRIORITY = ['pnpm', 'bun', 'yarn', 'npm'];

/**
 * Get the project configuration file path
 * @returns {string} Configuration file path
 */
function getProjectConfigPath() {
  const projectRoot = getProjectRoot();
  if (projectRoot) {
    return path.join(projectRoot, '.claude', 'package-manager.json');
  }
  return null;
}

/**
 * Get the global configuration file path
 * @returns {string} Configuration file path
 */
function getGlobalConfigPath() {
  return path.join(getClaudeConfigDir(), 'package-manager.json');
}

/**
 * Detect package manager from environment variables
 * @returns {string|null} Package manager name or null
 */
function detectFromEnvironment() {
  const envPm = process.env.CLAUDE_PACKAGE_MANAGER;
  if (envPm && PACKAGE_MANAGERS[envPm]) {
    return envPm;
  }
  return null;
}

/**
 * Detect package manager from project configuration
 * @returns {string|null} Package manager name or null
 */
function detectFromProjectConfig() {
  const configPath = getProjectConfigPath();
  if (configPath && fs.existsSync(configPath)) {
    const config = readJSON(configPath);
    if (config && config.packageManager && PACKAGE_MANAGERS[config.packageManager]) {
      return config.packageManager;
    }
  }
  return null;
}

/**
 * Detect package manager from global configuration
 * @returns {string|null} Package manager name or null
 */
function detectFromGlobalConfig() {
  const configPath = getGlobalConfigPath();
  if (configPath && fs.existsSync(configPath)) {
    const config = readJSON(configPath);
    if (config && config.packageManager && PACKAGE_MANAGERS[config.packageManager]) {
      return config.packageManager;
    }
  }
  return null;
}

/**
 * Detect package manager from package.json
 * @returns {string|null} Package manager name or null
 */
function detectFromPackageJson() {
  const projectRoot = getProjectRoot();
  if (!projectRoot) {
    return null;
  }

  const packageJsonPath = path.join(projectRoot, 'package.json');
  if (!fs.existsSync(packageJsonPath)) {
    return null;
  }

  const packageJson = readJSON(packageJsonPath);
  if (!packageJson) {
    return null;
  }

  // Check the packageManager field
  if (packageJson.packageManager) {
    // Format: "npm@8.0.0" or "pnpm@7.0.0"
    const match = packageJson.packageManager.match(/^([a-zA-Z]+)@/);
    if (match && PACKAGE_MANAGERS[match[1]]) {
      return match[1];
    }
  }

  return null;
}

/**
 * Detect package manager from lock file
 * @returns {string|null} Package manager name or null
 */
function detectFromLockFile() {
  const projectRoot = getProjectRoot();
  if (!projectRoot) {
    return null;
  }

  // Check lock files in priority order
  for (const pm of DETECTION_PRIORITY) {
    const lockFile = path.join(projectRoot, PACKAGE_MANAGERS[pm].lockFile);
    if (fs.existsSync(lockFile)) {
      return pm;
    }
  }

  return null;
}

/**
 * Detect package manager from available commands
 * @returns {string|null} Package manager name or null
 */
function detectFromAvailableCommands() {
  for (const pm of DETECTION_PRIORITY) {
    if (commandExists(pm)) {
      return pm;
    }
  }
  // npm is always available (bundled with Node.js)
  return 'npm';
}

/**
 * Intelligently detect the package manager
 * @param {Object} options - Detection options
 * @returns {{name: string, source: string, config: Object}} Detection result
 */
function getPackageManager(options = {}) {
  const {
    skipEnvironment = false,
    skipProjectConfig = false,
    skipGlobalConfig = false,
    skipPackageJson = false,
    skipLockFile = false,
    skipAvailable = false
  } = options;

  // Detect in priority order
  const detectors = [
    !skipEnvironment && { detector: detectFromEnvironment, source: 'environment' },
    !skipProjectConfig && { detector: detectFromProjectConfig, source: 'project-config' },
    !skipPackageJson && { detector: detectFromPackageJson, source: 'package.json' },
    !skipLockFile && { detector: detectFromLockFile, source: 'lock-file' },
    !skipGlobalConfig && { detector: detectFromGlobalConfig, source: 'global-config' },
    !skipAvailable && { detector: detectFromAvailableCommands, source: 'available' }
  ].filter(Boolean);

  for (const { detector, source } of detectors) {
    const pm = detector();
    if (pm && PACKAGE_MANAGERS[pm]) {
      return {
        name: pm,
        source,
        config: PACKAGE_MANAGERS[pm]
      };
    }
  }

  // Default fallback to npm
  return {
    name: 'npm',
    source: 'default',
    config: PACKAGE_MANAGERS.npm
  };
}

/**
 * Set the project package manager
 * @param {string} packageManager - Package manager name
 * @returns {boolean} Whether the operation succeeded
 */
function setProjectPackageManager(packageManager) {
  if (!PACKAGE_MANAGERS[packageManager]) {
    console.error(`Unsupported package manager: ${packageManager}`);
    return false;
  }

  const configPath = getProjectConfigPath();
  if (!configPath) {
    console.error('Cannot find project root directory');
    return false;
  }

  const configDir = path.dirname(configPath);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }

  try {
    fs.writeFileSync(
      configPath,
      JSON.stringify({ packageManager }, null, 2),
      'utf8'
    );
    return true;
  } catch (err) {
    console.error(`Failed to write configuration: ${err.message}`);
    return false;
  }
}

/**
 * Set the global package manager
 * @param {string} packageManager - Package manager name
 * @returns {boolean} Whether the operation succeeded
 */
function setGlobalPackageManager(packageManager) {
  if (!PACKAGE_MANAGERS[packageManager]) {
    console.error(`Unsupported package manager: ${packageManager}`);
    return false;
  }

  const configPath = getGlobalConfigPath();
  const configDir = path.dirname(configPath);

  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }

  try {
    fs.writeFileSync(
      configPath,
      JSON.stringify({ packageManager }, null, 2),
      'utf8'
    );
    return true;
  } catch (err) {
    console.error(`Failed to write configuration: ${err.message}`);
    return false;
  }
}

/**
 * Build a package manager command
 * @param {string} commandType - Command type (install, run, exec)
 * @param {Object} options - Options
 * @returns {string} Full command string
 */
function buildCommand(commandType, options = {}) {
  const pm = getPackageManager();
  const config = pm.config;

  switch (commandType) {
    case 'install':
      return config.installCmd;
    case 'run':
      return `${config.runCmd} ${options.script || ''}`;
    case 'exec':
      return `${config.execCmd} ${options.package || ''}`;
    default:
      return config.installCmd;
  }
}

/**
 * Get all available package managers
 * @returns {Array<{name: string, available: boolean}>} List of available package managers
 */
function getAvailablePackageManagers() {
  return Object.keys(PACKAGE_MANAGERS).map(name => ({
    name,
    available: commandExists(name)
  }));
}

/**
 * Print package manager information
 */
function printPackageManagerInfo() {
  const pm = getPackageManager();
  console.log(`Current package manager: ${pm.name} (source: ${pm.source})`);
  console.log(`Configuration:`);
  console.log(`  Install command: ${pm.config.installCmd}`);
  console.log(`  Run command: ${pm.config.runCmd}`);
  console.log(`  Exec command: ${pm.config.execCmd}`);
}

// Export all functions
module.exports = {
  PACKAGE_MANAGERS,
  DETECTION_PRIORITY,
  getPackageManager,
  setProjectPackageManager,
  setGlobalPackageManager,
  buildCommand,
  getAvailablePackageManagers,
  printPackageManagerInfo,
  getProjectConfigPath,
  getGlobalConfigPath,
  // Additional exports for setup-package-manager.js
  setPreferredPackageManager: setGlobalPackageManager,
  detectFromLockFile,
  detectFromPackageJson,
  getSelectionPrompt: () => {
    return '\n💡 Run /setup-pm to configure the preferred package manager\n';
  }
};
