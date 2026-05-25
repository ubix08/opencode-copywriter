# Topic Taxonomy & Audience Calibration

## Topic Categories

### Infrastructure & DevOps
- **Topics**: CI/CD, containers, orchestration, IaC, monitoring, cloud platforms
- **Default audience**: Intermediate
- **Voice**: Operational, reliability-focused, tradeoff-aware
- **Code emphasis**: Configuration files, deployment scripts, pipeline definitions
- **Key signals**: Uptime, cost, scalability, security posture

### APIs & Backend Development
- **Topics**: REST, GraphQL, gRPC, authentication, rate limiting, caching, databases
- **Default audience**: Intermediate to Advanced
- **Voice**: Precision-focused, specification-aware, performance-conscious
- **Code emphasis**: Endpoint definitions, request/response examples, error handling
- **Key signals**: Latency, throughput, correctness, versioning strategy

### Frontend & UI Engineering
- **Topics**: Frameworks, state management, rendering, accessibility, performance
- **Default audience**: Intermediate
- **Voice**: User-experience-aware, pattern-driven, browser-reality-grounded
- **Code emphasis**: Component code, hooks, styling, build configuration
- **Key signals**: Load time, bundle size, accessibility score, Core Web Vitals

### AI & Machine Learning
- **Topics**: LLMs, embeddings, RAG, fine-tuning, evaluation, deployment
- **Default audience**: Intermediate
- **Voice**: Experiment-driven, metric-aware, honest about limitations
- **Code emphasis**: Model calls, prompt templates, evaluation scripts, data pipelines
- **Key signals**: Accuracy, latency, cost per token, hallucination rate

### Security & Compliance
- **Topics**: Authentication, encryption, vulnerability management, audits, standards
- **Default audience**: Advanced
- **Voice**: Risk-aware, specification-precise, consequence-conscious
- **Code emphasis**: Security configurations, audit scripts, policy definitions
- **Key signals**: CVE coverage, compliance level, attack surface reduction

### Developer Experience & Tooling
- **Topics**: CLI tools, IDEs, debugging, testing, documentation, package management
- **Default audience**: Beginner to Intermediate
- **Voice**: Practical, workflow-focused, opinionated but fair
- **Code emphasis**: Command examples, configuration, plugin setup
- **Key signals**: Time saved, error reduction, learning curve

## Audience Skill Levels

### Beginner
- **Assume**: Knows programming basics, unfamiliar with the specific topic
- **Define**: Every technical term on first use
- **Show**: Full commands, complete code examples, step-by-step instructions
- **Explain**: Concepts and "why" behind recommendations
- **Avoid**: Jargon without definition, skipped steps, assumed context

### Intermediate (Default)
- **Assume**: Comfortable with general programming, learning specific tools/patterns
- **Define**: Domain-specific terms, not general programming concepts
- **Show**: Focused examples, skip boilerplate unless relevant
- **Explain**: Tradeoffs, patterns, when to use which approach
- **Avoid**: Basic tutorials, hand-holding through obvious steps

### Advanced
- **Assume**: Deep experience with the domain, looking for edge cases and optimization
- **Define**: Nothing unless it's a new or niche concept
- **Show**: Benchmarks, architecture diagrams, source code references, failure modes
- **Explain**: Internal mechanics, performance characteristics, alternative approaches
- **Avoid**: Setup instructions, basic explanations, introductory content

## Calibration Rules

1. **Default to intermediate** unless the topic or request specifies otherwise
2. **Adjust based on topic category**: Security topics lean advanced, DevEx topics lean beginner
3. **When in doubt, include a skill-level note** at the top: "This guide assumes familiarity with [prerequisite]"
4. **Mixed audiences**: Write for intermediate, include "For beginners" callout boxes and "Advanced" sections
