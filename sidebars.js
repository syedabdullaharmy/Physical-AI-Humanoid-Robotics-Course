/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // Main tutorial sidebar with nested collapsible categories
  tutorialSidebar: [
    'setup',
    {
      type: 'category',
      label: 'Module 1: ROS 2 Foundations',
      collapsible: true,
      collapsed: false,
      items: [
        'module-1-ros2/introduction',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 Foundations',
      collapsible: true,
      collapsed: false,
      items: [
        'module-1-ros2/introduction',
      ],
    },
  ],
};

export default sidebars;
