
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
    'primary': '#333',
    'secondary': '#666',
    'accent': '#2563eb',
    'background': '#2c3e50',
    'dark-primary': '#2854b0',
    'dark-secondary': '#111719',
    'dark-accent': '#7962e5',
    'dark-background': '#070a17'
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