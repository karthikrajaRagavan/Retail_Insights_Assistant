const pptxgen = require('pptxgenjs');
const path = require('path');

// Import html2pptx from the skill location
const html2pptx = require('C:/Users/kr3258345/.claude/plugins/marketplaces/anthropic-agent-skills/skills/pptx/scripts/html2pptx.js');

async function createPresentation() {
    const pptx = new pptxgen();

    // Set presentation properties
    pptx.layout = 'LAYOUT_16x9';
    pptx.title = 'Retail Insights Assistant - Architecture Presentation';
    pptx.author = 'AI Architect';
    pptx.subject = 'GenAI Multi-Agent System for Enterprise Analytics';
    pptx.company = 'Blend360 Interview';

    const slideDir = __dirname;

    const slides = [
        { file: 'slide01-title.html', name: 'Title' },
        { file: 'slide02-executive-summary.html', name: 'Executive Summary' },
        { file: 'slide03-architecture-overview.html', name: 'Architecture Overview' },
        { file: 'slide04-multi-agent-design.html', name: 'Multi-Agent Design' },
        { file: 'slide05-technology-rationale.html', name: 'Technology Rationale' },
        { file: 'slide06-security-guardrails.html', name: 'Security & Guardrails' },
        { file: 'slide07-query-pipeline.html', name: 'Query Pipeline' },
        { file: 'slide08-data-engineering.html', name: 'Data Engineering' },
        { file: 'slide09-scale-architecture.html', name: 'Scale Architecture' },
        { file: 'slide10-scale-dataflow.html', name: 'Scale Dataflow' },
        { file: 'slide11-observability.html', name: 'Observability' },
        { file: 'slide12-cost-analysis.html', name: 'Cost Analysis' },
        { file: 'slide13-limitations-roadmap.html', name: 'Limitations & Roadmap' },
        { file: 'slide14-summary.html', name: 'Summary' }
    ];

    for (let i = 0; i < slides.length; i++) {
        const slide = slides[i];
        console.log(`Processing slide ${i + 1}/${slides.length}: ${slide.name}...`);
        await html2pptx(path.join(slideDir, slide.file), pptx);
    }

    // Save the presentation
    const outputPath = path.join(slideDir, '..', 'Retail_Insights_Architecture_V2.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`\nPresentation created: ${outputPath}`);
}

createPresentation().catch(err => {
    console.error('Error creating presentation:', err);
    process.exit(1);
});
