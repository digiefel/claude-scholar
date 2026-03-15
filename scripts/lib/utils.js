/**
 * Cross-platform utility library
 * Provides cross-platform compatibility support for Claude Code plugins
 *
 * @module utils
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync, spawnSync } = require('child_process');

// Platform detection constants
const isWindows = process.platform === 'win32';
const isMacOS = process.platform === 'darwin';
const isLinux = process.platform === 'linux';

/**
 * Get the user home directory (cross-platform)
 * @returns {string} User home directory path
 */
function getHomeDir() {
  return os.homedir();
}

/**
 * Ensure a directory exists, creating it if it does not (cross-platform)
 * @param {string} dirPath - Directory path
 * @returns {string} Directory path
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  return dirPath;
}

/**
 * Check whether a command exists (cross-platform)
 * @param {string} cmd - Command name
 * @returns {boolean} Whether the command exists
 */
function commandExists(cmd) {
  // Validate command name safety
  if (!/^[a-zA-Z0-9_.-]+$/.test(cmd)) {
    return false;
  }

  try {
    if (isWindows) {
      // Windows uses the where command
      const result = spawnSync('where', [cmd], { stdio: 'pipe' });
      return result.status === 0;
    } else {
      // Unix-like systems use the which command
      const result = spawnSync('which', [cmd], { stdio: 'pipe' });
      return result.status === 0;
    }
  } catch {
    return false;
  }
}

/**
 * Safely execute a command (cross-platform)
 * @param {string} cmd - Command to execute
 * @param {Object} options - Execution options
 * @returns {{success: boolean, output: string, error?: string}} Execution result
 */
function runCommand(cmd, options = {}) {
  try {
    const result = execSync(cmd, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
      ...options
    });
    return { success: true, output: result.trim() };
  } catch (err) {
    return {
      success: false,
      output: err.stdout || '',
      error: err.stderr || err.message
    };
  }
}

/**
 * Get the Claude configuration directory (cross-platform)
 * @returns {string} Claude configuration directory path
 */
function getClaudeConfigDir() {
  const homeDir = getHomeDir();
  return path.join(homeDir, '.claude');
}

/**
 * Get the project root directory (cross-platform)
 * @param {string} startDir - Starting directory
 * @returns {string|null} Project root directory or null
 */
function getProjectRoot(startDir = process.cwd()) {
  let currentDir = startDir;

  while (currentDir !== path.parse(currentDir).root) {
    // Check whether .claude-plugin directory exists
    const pluginDir = path.join(currentDir, '.claude-plugin');
    if (fs.existsSync(pluginDir)) {
      return currentDir;
    }

    // Check whether package.json exists
    const packageJson = path.join(currentDir, 'package.json');
    if (fs.existsSync(packageJson)) {
      return currentDir;
    }

    // Move up one level
    currentDir = path.dirname(currentDir);
  }

  return null;
}

/**
 * Join path segments (cross-platform)
 * @param {...string} paths - Path segments
 * @returns {string} Joined path
 */
function joinPath(...paths) {
  return path.join(...paths);
}

/**
 * Resolve an absolute path (cross-platform)
 * @param {...string} paths - Path segments
 * @returns {string} Absolute path
 */
function resolvePath(...paths) {
  return path.resolve(...paths);
}

/**
 * Normalize a path (cross-platform)
 * @param {string} filePath - File path
 * @returns {string} Normalized path
 */
function normalizePath(filePath) {
  return path.normalize(filePath);
}

/**
 * Read a JSON file (cross-platform)
 * @param {string} filePath - JSON file path
 * @returns {Object|null} Parsed JSON object or null
 */
function readJSON(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  } catch {
    return null;
  }
}

/**
 * Write a JSON file (cross-platform)
 * @param {string} filePath - JSON file path
 * @param {Object} data - Data to write
 * @param {number|object|string} space - JSON indentation spaces
 * @returns {boolean} Whether the operation succeeded
 */
function writeJSON(filePath, data, space = 2) {
  try {
    ensureDir(path.dirname(filePath));
    fs.writeFileSync(filePath, JSON.stringify(data, null, space), 'utf8');
    return true;
  } catch {
    return false;
  }
}

/**
 * Copy a file (cross-platform)
 * @param {string} src - Source file path
 * @param {string} dest - Destination file path
 * @returns {boolean} Whether the operation succeeded
 */
function copyFile(src, dest) {
  try {
    ensureDir(path.dirname(dest));
    fs.copyFileSync(src, dest);
    return true;
  } catch {
    return false;
  }
}

/**
 * Get platform information
 * @returns {Object} Platform information object
 */
function getPlatformInfo() {
  return {
    platform: process.platform,
    isWindows,
    isMacOS,
    isLinux,
    arch: process.arch,
    nodeVersion: process.version,
    homeDir: getHomeDir(),
    tempDir: os.tmpdir()
  };
}

// Export all functions
module.exports = {
  isWindows,
  isMacOS,
  isLinux,
  getHomeDir,
  ensureDir,
  commandExists,
  runCommand,
  getClaudeConfigDir,
  getProjectRoot,
  joinPath,
  resolvePath,
  normalizePath,
  readJSON,
  writeJSON,
  copyFile,
  getPlatformInfo
};
