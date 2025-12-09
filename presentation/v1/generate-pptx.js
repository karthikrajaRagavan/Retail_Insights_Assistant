const pptxgen = require('pptxgenjs');
const path = require('path');

// Import html2pptx from the skill location
const html2pptx = require('C:/Users/kr3258345/.claude/plugins/marketplaces/anthropic-agent-skills/skills/pptx/scripts/html2pptx.js');

async function createPresentation() {
    const pptx = new pptxgen();

    // Set presentation properties
    pptx.layout = 'LAYOUT_16x9';
    pptx.title = 'Retail Insights Assistant - Architecture';
    pptx.author = 'Blend360 AI Architect';
    pptx.subject = 'GenAI-Powered Multi-Agent Analytics System';

    const slideDir = __dirname;

    // Slide 1: Title
    console.log('Processing slide 1: Title...');
    await html2pptx(path.join(slideDir, 'slide01-title.html'), pptx);

    // Slide 2: Problem & Solution
    console.log('Processing slide 2: Problem & Solution...');
    await html2pptx(path.join(slideDir, 'slide02-problem.html'), pptx);

    // Slide 3: System Architecture
    console.log('Processing slide 3: System Architecture...');
    await html2pptx(path.join(slideDir, 'slide03-architecture.html'), pptx);

    // Slide 4: Multi-Agent Design
    console.log('Processing slide 4: Multi-Agent Design...');
    await html2pptx(path.join(slideDir, 'slide04-agents.html'), pptx);

    // Slide 5: Technology Stack
    console.log('Processing slide 5: Technology Stack...');
    await html2pptx(path.join(slideDir, 'slide05-tech-stack.html'), pptx);

    // Slide 6: Data Layer
    console.log('Processing slide 6: Data Layer...');
    await html2pptx(path.join(slideDir, 'slide06-data-layer.html'), pptx);

    // Slide 7: Query-Response Pipeline
    console.log('Processing slide 7: Query-Response Pipeline...');
    await html2pptx(path.join(slideDir, 'slide07-pipeline.html'), pptx);

    // Slide 8: Scaling to 100GB+
    console.log('Processing slide 8: Scaling to 100GB+...');
    await html2pptx(path.join(slideDir, 'slide08-scale.html'), pptx);

    // Slide 9: Cost & Performance
    console.log('Processing slide 9: Cost & Performance...');
    await html2pptx(path.join(slideDir, 'slide09-cost.html'), pptx);

    // Slide 10: Summary
    console.log('Processing slide 10: Summary...');
    await html2pptx(path.join(slideDir, 'slide10-summary.html'), pptx);

    // Save the presentation
    const outputPath = path.join(slideDir, 'Retail_Insights_Architecture.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`\nPresentation created: ${outputPath}`);
}

createPresentation().catch(err => {
    console.error('Error creating presentation:', err);
    process.exit(1);
});
