class KnowledgeGraphVisualizer {
    constructor() {
        this.graphData = {
            nodes: [],
            edges: [],
        };
        this.categories = {};
        this.init();
    }

    async init() {
        await this.loadGraphData();
        this.createGraphCanvas();
        this.loadD3Library();
    }

    async loadGraphData() {
        try {
            const response = await fetch('./data/search-index.json');
            const articles = await response.json();

            this.buildGraphStructure(articles);
        } catch (error) {
            console.error('加载图谱数据失败:', error);
        }
    }

    buildGraphStructure(articles) {
        const categoryMap = {};

        articles.forEach((article) => {
            const nodeId = `node-${this.graphData.nodes.length}`;

            this.graphData.nodes.push({
                id: nodeId,
                label: article.title,
                category: article.category,
                url: article.url,
                keywords: article.keywords?.split(' ') || [],
                size: 10,
                color: this.getCategoryColor(article.category),
            });

            if (article.category) {
                if (!categoryMap[article.category]) {
                    categoryMap[article.category] = [];
                }
                categoryMap[article.category].push(nodeId);
            }
        });

        this.categories = categoryMap;

        this.buildEdges(articles);
    }

    getCategoryColor(category) {
        const colors = {
            Python: '#3b82f6',
            前端: '#10b981',
            React: '#06b6d4',
            'Vue.js': '#8b5cf6',
            TypeScript: '#f59e0b',
            DevOps: '#ef4444',
            'Node.js': '#84cc16',
            工具: '#ec4899',
            后端: '#14b8a6',
        };

        return colors[category] || '#6b7280';
    }

    buildEdges(articles) {
        articles.forEach((article, index) => {
            const keywords = article.keywords?.split(' ') || [];

            articles.forEach((otherArticle, otherIndex) => {
                if (index >= otherIndex) return;

                const otherKeywords = otherArticle.keywords?.split(' ') || [];
                const commonKeywords = keywords.filter((k) => otherKeywords.includes(k));

                if (
                    commonKeywords.length >= 2 ||
                    (article.category === otherArticle.category && commonKeywords.length >= 1)
                ) {
                    this.graphData.edges.push({
                        source: `node-${index}`,
                        target: `node-${otherIndex}`,
                        strength: commonKeywords.length,
                    });
                }
            });
        });
    }

    createGraphCanvas() {
        const graphContainer = document.createElement('div');
        graphContainer.id = 'knowledge-graph';
        graphContainer.className = 'knowledge-graph-container';
        graphContainer.innerHTML = `
      <div class="graph-header">
        <h3><i class="fas fa-project-diagram"></i> 知识图谱</h3>
        <div class="graph-controls">
          <button class="graph-btn" id="reset-graph">
            <i class="fas fa-redo"></i> 重置
          </button>
          <button class="graph-btn" id="zoom-in">
            <i class="fas fa-search-plus"></i> 放大
          </button>
          <button class="graph-btn" id="zoom-out">
            <i class="fas fa-search-minus"></i> 缩小
          </button>
        </div>
      </div>
      <div class="graph-canvas" id="graph-canvas"></div>
      <div class="graph-info">
        <div class="graph-stats">
          <span class="stat-item">
            <i class="fas fa-circle"></i> ${this.graphData.nodes.length} 个知识点
          </span>
          <span class="stat-item">
            <i class="fas fa-link"></i> ${this.graphData.edges.length} 个关联
          </span>
        </div>
        <div class="category_legend">
          ${Object.keys(this.categories)
              .map(
                  (cat) => `
            <span class="legend-item">
              <span class="legend-color" style="background: ${this.getCategoryColor(cat)}"></span>
              ${cat}
            </span>
          `
              )
              .join('')}
        </div>
      </div>
    `;

        const navPage = document.querySelector('.nav-page') || document.querySelector('main');
        if (navPage && window.location.pathname.includes('nav.html')) {
            navPage.appendChild(graphContainer);
            this.addGraphStyles();
            this.graphCanvas = graphContainer.querySelector('#graph-canvas');
        }
    }

    addGraphStyles() {
        const style = document.createElement('style');
        style.textContent = `
      .knowledge-graph-container {
        background: var(--bg-color);
        border-radius: 12px;
        padding: 24px;
        margin-top: 40px;
        border: 1px solid var(--border-color);
      }
      
      .graph-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
      }
      
      .graph-header h3 {
        margin: 0;
        font-size: 24px;
        color: var(--text-color);
        display: flex;
        align-items: center;
        gap: 12px;
      }
      
      .graph-controls {
        display: flex;
        gap: 12px;
      }
      
      .graph-btn {
        background: var(--bg-secondary-color);
        border: 1px solid var(--border-color);
        color: var(--text-color);
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
      }
      
      .graph-btn:hover {
        border-color: var(--primary-color);
        color: var(--primary-color);
      }
      
      .graph-canvas {
        width: 100%;
        height: 600px;
        border-radius: 8px;
        background: var(--bg-secondary-color);
        position: relative;
        overflow: hidden;
      }
      
      .graph-info {
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      
      .graph-stats {
        display: flex;
        gap: 16px;
      }
      
      .stat-item {
        font-size: 14px;
        color: var(--text-secondary-color);
        display: flex;
        align-items: center;
        gap: 6px;
      }
      
      .category_legend {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
      }
      
      .legend-item {
        font-size: 13px;
        color: var(--text-secondary-color);
        display: flex;
        align-items: center;
        gap: 6px;
      }
      
      .legend-color {
        width: 12px;
        height: 12px;
        border-radius: 50%;
      }
      
      .node-circle {
        cursor: pointer;
        transition: all 0.2s;
      }
      
      .node-circle:hover {
        filter: brightness(1.2);
      }
      
      .node-label {
        font-size: 12px;
        color: var(--text-color);
        pointer-events: none;
      }
      
      .edge-line {
        stroke: rgba(100, 100, 100, 0.3);
        stroke-width: 1;
        opacity: 0.5;
      }
      
      .dark-mode .knowledge-graph-container {
        background: #1f2937;
        border-color: #374151;
      }
      
      .dark-mode .graph-canvas {
        background: #111827;
      }
      
      .dark-mode .graph-btn {
        background: #374151;
        border-color: #4b5563;
        color: #f9fafb;
      }
      
      .dark-mode .edge-line {
        stroke: rgba(200, 200, 200, 0.3);
      }
      
      @media (max-width: 768px) {
        .graph-canvas {
          height: 400px;
        }
        
        .graph-header {
          flex-direction: column;
          gap: 12px;
          align-items: flex-start;
        }
        
        .graph-info {
          flex-direction: column;
          gap: 12px;
        }
        
        .category_legend {
          justify-content: center;
        }
      }
    `;
        document.head.appendChild(style);
    }

    async loadD3Library() {
        if (window.d3) {
            this.renderGraph();
            return;
        }

        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js';
        script.integrity =
            'sha512-M7nZ5JMn0ppsZt4X7Ek9ShkzkLYJU0G8GvJtGdN+eqL3Uo1fF5qkvsZt4X7Ek9ShkzkLYJU0G8GvJtGdN+eqL3Uo1fF5qkvsZ';
        script.crossOrigin = 'anonymous';

        script.onload = () => {
            this.renderGraph();
        };

        document.head.appendChild(script);
    }

    renderGraph() {
        if (!window.d3 || !this.graphCanvas) return;

        const width = this.graphCanvas.clientWidth;
        const height = this.graphCanvas.clientHeight;

        const svg = d3
            .select(this.graphCanvas)
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        const simulation = d3
            .forceSimulation(this.graphData.nodes)
            .force(
                'link',
                d3
                    .forceLink(this.graphData.edges)
                    .id((d) => d.id)
                    .distance(50)
            )
            .force('charge', d3.forceManyBody().strength(-100))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(20));

        const edges = svg
            .append('g')
            .selectAll('line')
            .data(this.graphData.edges)
            .enter()
            .append('line')
            .attr('class', 'edge-line');

        const nodes = svg
            .append('g')
            .selectAll('circle')
            .data(this.graphData.nodes)
            .enter()
            .append('circle')
            .attr('class', 'node-circle')
            .attr('r', (d) => d.size)
            .attr('fill', (d) => d.color)
            .call(d3.drag().on('start', dragstarted).on('drag', dragged).on('end', dragended));

        const labels = svg
            .append('g')
            .selectAll('text')
            .data(this.graphData.nodes)
            .enter()
            .append('text')
            .attr('class', 'node-label')
            .attr('text-anchor', 'middle')
            .attr('dy', -15)
            .text((d) => d.label.substring(0, 20));

        simulation.on('tick', () => {
            edges
                .attr('x1', (d) => d.source.x)
                .attr('y1', (d) => d.source.y)
                .attr('x2', (d) => d.target.x)
                .attr('y2', (d) => d.target.y);

            nodes.attr('cx', (d) => d.x).attr('cy', (d) => d.y);

            labels.attr('x', (d) => d.x).attr('y', (d) => d.y);
        });

        nodes.on('click', (event, d) => {
            window.location.href = d.url;
        });

        nodes
            .on('mouseover', (event, d) => {
                labels
                    .filter((l) => l.id === d.id)
                    .style('font-weight', 'bold')
                    .style('font-size', '14px');
            })
            .on('mouseout', (event, d) => {
                labels
                    .filter((l) => l.id === d.id)
                    .style('font-weight', 'normal')
                    .style('font-size', '12px');
            });

        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        this.bindControlEvents(simulation, svg);
    }

    bindControlEvents(simulation, svg) {
        document.getElementById('reset-graph')?.addEventListener('click', () => {
            simulation.alpha(1).restart();
        });

        document.getElementById('zoom-in')?.addEventListener('click', () => {
            svg.transition()
                .duration(300)
                .call(
                    d3.zoom().on('zoom', (event) => {
                        svg.selectAll('g').attr('transform', event.transform);
                    }).scaleBy,
                    1.2
                );
        });

        document.getElementById('zoom-out')?.addEventListener('click', () => {
            svg.transition()
                .duration(300)
                .call(
                    d3.zoom().on('zoom', (event) => {
                        svg.selectAll('g').attr('transform', event.transform);
                    }).scaleBy,
                    0.8
                );
        });
    }
}

const knowledgeGraphVisualizer = new KnowledgeGraphVisualizer();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = KnowledgeGraphVisualizer;
}
