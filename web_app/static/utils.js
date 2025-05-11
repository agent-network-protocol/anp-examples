/**
 * Utility functions for the ANP Explorer application
 */

/**
 * Get the base path for API requests based on the current deployment environment
 * This function automatically detects whether the application is deployed at
 * root level or in a subdirectory
 * 
 * @return {string} The base path for API requests
 */
function getBasePath() {
  // Get the current URL's origin (protocol + domain + port)
  const origin = window.location.origin;
  
  // Get application root path
  // If there's a specific path identifier (like 'anp-explorer' or 'anp-demo'), use it
  const pathSegments = window.location.pathname.split('/').filter(segment => segment);
  
  // Check for known application identifiers
  const appIdentifiers = ['anp-explorer', 'anp-demo'];
  
  // Find the first matching app identifier in the path
  for (const identifier of appIdentifiers) {
    const appPathIndex = pathSegments.indexOf(identifier);
    if (appPathIndex !== -1) {
      // Found a valid app identifier, return the path up to and including it
      return `${origin}/${pathSegments.slice(0, appPathIndex + 1).join('/')}`;
    }
  }
  
  // If no application identifier is found, or if deployed at root, return just the origin
  return origin;
}
