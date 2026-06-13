// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';

export default defineConfig({
  markdown: {
    gfm: true,
  },
  integrations: [
    starlight({
      title: 'Software Design for Programmers & AI Coding Agents',
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/Lightbridge-KS',
        },
      ],
      sidebar: [
        {
          label: 'Part I - Foundations',
          collapsed: false,
          items: [
            { label: 'Overview', slug: 'part-1-foundations' },
            { label: '1. Design Is Communication', slug: 'part-1-foundations/01-design-is-communication' },
            { label: '2. Change and Complexity', slug: 'part-1-foundations/02-change-and-complexity' },
            { label: '3. The Design Loop with AI', slug: 'part-1-foundations/03-design-loop-with-ai' },
          ],
        },
        {
          label: 'Part II - Principles',
          collapsed: false,
          items: [
            { label: 'Overview', slug: 'part-2-principles' },
            { label: '4. Cohesion and SRP', slug: 'part-2-principles/04-cohesion-and-srp' },
            { label: '5. Coupling and Least Knowledge', slug: 'part-2-principles/05-coupling-and-least-knowledge' },
            { label: '6. Encapsulation and Information Hiding', slug: 'part-2-principles/06-encapsulation-and-information-hiding' },
            { label: '7. Least Astonishment and Contracts', slug: 'part-2-principles/07-least-astonishment-and-contracts' },
            { label: '8. Extension Without Modification', slug: 'part-2-principles/08-extension-without-modification' },
            { label: '9. YAGNI, KISS, and Right-Sizing', slug: 'part-2-principles/09-yagni-kiss-right-sizing' },
          ],
        },
        {
          label: 'Part III - Patterns',
          collapsed: false,
          items: [
            { label: 'Overview', slug: 'part-3-patterns' },
            {
              label: 'Creational',
              items: [
                { label: '10. Factories and Singleton', slug: 'part-3-patterns/10-factories' },
              ],
            },
            {
              label: 'Structural',
              items: [
                { label: '11. Adapter and Façade', slug: 'part-3-patterns/11-adapter-and-facade' },
                { label: '12. Composite and Decorator', slug: 'part-3-patterns/12-composite-and-decorator' },
              ],
            },
            {
              label: 'Behavioral',
              items: [
                { label: '13. Strategy and Template Method', slug: 'part-3-patterns/13-strategy-and-template-method' },
                { label: '14. Observer and State', slug: 'part-3-patterns/14-observer-and-state' },
                { label: '15. Iterator and Visitor', slug: 'part-3-patterns/15-iterator-visitor-python-replacements' },
              ],
            },
          ],
        },
        {
          label: 'Part IV - Codebase Design',
          collapsed: false,
          items: [
            { label: 'Overview', slug: 'part-4-codebase-design' },
            { label: '16. Modules and Packages', slug: 'part-4-codebase-design/16-modules-and-packages' },
            { label: '17. Dependency Direction and Three Tiers', slug: 'part-4-codebase-design/17-dependency-direction-and-three-tiers' },
            { label: '18. Tests as Design Contracts', slug: 'part-4-codebase-design/18-tests-as-design-contracts' },
          ],
        },
        {
          label: 'Part V - AI Partnership',
          collapsed: false,
          items: [
            { label: 'Overview', slug: 'part-5-ai-partnership' },
            { label: '19. The Prompt Phrasebook', slug: 'part-5-ai-partnership/19-prompt-phrasebook' },
            { label: '20. Agent Conventions', slug: 'part-5-ai-partnership/20-agent-conventions' },
            { label: '21. Reviewing AI-Generated Code', slug: 'part-5-ai-partnership/21-reviewing-ai-generated-code' },
            { label: '22. Refactoring as a Dialogue', slug: 'part-5-ai-partnership/22-refactoring-as-dialogue' },
          ],
        },
        {
          label: 'Appendices',
          collapsed: false,
          items: [
            { label: 'Overview', slug: 'appendices' },
            { label: 'A. The Design Glossary-Phrasebook', slug: 'appendices/a-design-glossary-phrasebook' },
            { label: 'B. Prompt Template Library', slug: 'appendices/b-prompt-template-library' },
            { label: 'C. Mermaid Cookbook for Design Docs', slug: 'appendices/c-mermaid-cookbook' },
            { label: 'D. Building This Book', slug: 'appendices/d-building-this-book' },
          ],
        },
      ],
    }),
    mermaid({
      theme: 'forest',
      autoTheme: true,
    }),
  ],
});
