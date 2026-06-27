explorer_html_string = """
<!doctype html>
<html lang="en">

  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, minimum-scale=1, initial-scale=1, user-scalable=yes">
    <title>OpenAPI Explorer</title>
    <link rel="shortcut icon" href="explorer/images/explorer.svg">
    <link rel="stylesheet" href="explorer/css/default.min.css">
    <link rel="stylesheet" href="explorer/css/bootstrap.min.css">
    <link rel="stylesheet" href="explorer/css/all.min.css">

    <script src="explorer/js/openapi-explorer.min.js" type="module" defer></script>

    <style>
      html, body {
        height: 100%
      }

      :root {
        --primary: #1D2F3B;
        --secondary: #FBAF0B;
        --dark: #000515;
        --horizon: #DEE2E6;
        --light: #FFFFFF;
        --gray: #465865;
        --info: #FFFFFF;
        --border: #98A1A9;
        --embossed: #A9D2E9;
        --highlight: #DC7100;
      }

      :openapi-explorer {
        --primary: #1D2F3B;
        --secondary: #FBAF0B;
        --dark: #000515;
        --horizon: #DEE2E6;
        --light: #FFFFFF;
        --gray: #465865;
        --info: #FFFFFF;
        --border: #98A1A9;
        --embossed: #A9D2E9;
        --highlight: #DC7100;
      }
      openapi-explorer {
        height: calc(100% - 56px);
      }

      .fixed-in-bottom-corner {
        z-index: 100;
        position: fixed;
        bottom: .5em;
        right: 1.5em;
      }

      .contact-us {
        cursor: pointer;
      }
      .contact-us > * {
        color: var(--light);
        background-color: var(--primary) !important;
      }
      .badge {
        font-size: inherit;
        height: 2rem;
        border-radius: 100px;
        padding: 0 0.75rem;
      }
    </style>
  </head>

  <body>
    <nav class="navbar navbar-dark bg-dark">
      <div class="container-fluid w-100 d-flex justify-content-between align-items-center">
        <div class="">
          <div class="navbar-brand d-none d-sm-inline-flex align-items-center" href="#">
            <img src="explorer/images/explorer-text.svg" alt="" height="24" class="d-none d-md-inline-block align-text-top me-2">
            <span>OpenAPI Explorer</span>
          </div>
        </div>
        <form id="loadSpecForm" class="d-flex">
          <input id="specUrl" class="form-control me-2" type="search" placeholder="Your OpenAPI url here" aria-label="SpecUrl" style="max-width: 400px">
          <div class="d-flex align-items-center">
            <button id="loadButton" class="btn btn-primary btn-sm" type="submit">Load</button>
          </div>
        </form>
      </div>
    </nav>
    <openapi-explorer spec-url="" collapse table schema-description-expanded="true" nav-item-spacing="compact" show-components="true" bg-color="#FFFFFF" header-bg-color="#DEE2E6" nav-bg-color="#1D2F3B" text-color="#465865" nav-hover-text-color="#FFFFFF"
    primary-color="#1D2F3B" secondary-color="#FBAF0B">
      <slot name="overview">
        <div class="alert alert-primary d-flex align-items-center m-4" role="alert">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2" viewBox="0 0 16 16" role="img" aria-label="Warning:">
            <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
          </svg>
          <small>
            The Authress API is an example OpenAPI loaded to show how the OpenAPI Explorer works. Try it out with your own OpenAPI spec, but using the load url in the navigation bar at the top of the screen.
          </small>
        </div>
      </slot>
    </openapi-explorer>

    <script>
      document.addEventListener('DOMContentLoaded', async (event) => {
        const specUrl = document.getElementById('specUrl');
        specUrl.value = '{{ doc_url }}';
        
        const explorerElement = document.getElementsByTagName("openapi-explorer")[0];
        explorerElement.setAttribute('spec-url', specUrl.value);
        
        const explorer_config = JSON.parse(`{{ explorer_config|default('{}')|tojson }}`);
        if (explorer_config && typeof explorer_config === 'object') {
        for (const [key, value] of Object.entries(explorer_config)) {
            const attrValue = typeof value === 'boolean' ? String(value) : value;
            explorerElement.setAttribute(key, attrValue);
            }
        }

        const loadButton = document.getElementById('loadButton');
        loadButton.addEventListener('click', () => {
          try {
            const newUrl = new URL(window.location);
            newUrl.searchParams.set('url', specUrl.value);
            window.location.assign(newUrl.toString());
            document.getElementsByTagName("openapi-explorer")[0].setAttribute('spec-url', specUrl.value);
          } catch (error) {
            console.error('Failed to set spec url into url address bar', error);
          }
        });
      });
    </script>
  </body>

</html>

"""
