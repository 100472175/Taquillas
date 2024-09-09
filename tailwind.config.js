
import { join } from 'path';

// 1. Import the Skeleton plugin
import { skeleton } from '@skeletonlabs/tw-plugin';

const config = {
 // 2. Opt for dark mode to be handled via the class method
 darkMode: 'class',
 content: [
  './src/**/*.{html,js,svelte,ts}',
  // 3. Append the path to the Skeleton package
  join(require.resolve('@skeletonlabs/skeleton'), '../**/*.{html,js,svelte,ts}'),
  './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'
 ],
 theme: {
  extend: {
   fontFamily: {
    montserrat: ['Montserrat', 'sans-serif']
   },
   keyframes: {
    appear: {
     '0%': { marginLeft: '-50vw' },
     '100%': { marginLeft: '0vw' }
    },
    disappear: {
     '0%': { marginLeft: '0vw' },
     '100%': { marginLeft: '-50vw' }
    }
   },
   animation: {
    appear: 'appear 0.8s 1',
    disappear: 'disappear 0.8s 1'
   },
   colors: {
    'primary': '#333',  // #303030 -- Gris oscuro
    'secondary': '#666',  //#070a17 -- Gris claro
    'accent': '#2563eb',  // #2563eb -- Azul electrico claro
    'background': '#2c3e50',  // #2c3e50 -- Azul grisaceo
    'dark-primary': '#2854b0',  // #2854b0 -- Azul  oscuro
    'dark-secondary': '#111719',  // #111719 -- Negro
    'dark-accent': '#7962e5',   // #7962e5 -- Morado
    'dark-background': '#070a17',  // #070a17 -- Negro
    'dele-color': '#3BC4A0', // Color de la delegación EPS
    'dele-accent': '#FF6D2E', // Color de acento de la delegación EPS
    'dele-accent-hove': '#ff8647', 
                    
      },
   
  },
 },
 plugins: [
  // 4. Append the Skeleton plugin (after other plugins)
  require('flowbite/plugin'),
  skeleton
 ]
};

export default config;