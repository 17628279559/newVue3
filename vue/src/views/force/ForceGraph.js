import * as d3 from 'd3'

const ForceGraph = ({
    nodes,
    links
}, {
    nodeId = d => d.id,
    nodeGroup,
    nodeStrokeWidth = 3,
    nodeStrokeOpacity = 1,
    nodeRadius = 22,
    linkSource = ({ source }) => source,
    linkTarget = ({ target }) => target,
    colors = d3.schemeCategory10,
    width,
    height,
} = {}) => {
    const linkArc = (d) => {
        let re = nodeRadius
        if (d.target.id == "祁同伟" || d.target.id == "高育良" || d.target.id == "侯亮平")
            re = nodeRadius * 1.4
        const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
        return `
          M${d.source.x},${d.source.y}
          L${d.target.x + ((d.source.x - d.target.x) / r) * (re * 0.8)},${d.target.y + ((d.source.y - d.target.y) / r) * (re * 0.8)}
        `;
    }
    const ticked = () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y)
            .attr("d", linkArc);
        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
    }
    const intern = (value) => {
        return value !== null && typeof value === "object" ? value.valueOf() : value;
    }
    const drag = (simulation) => {
        const dragstarted = (event) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        const dragged = (event) => {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        const dragended = (event) => {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    const N = d3.map(nodes, nodeId).map(intern);
    const LS = d3.map(links, linkSource).map(intern);
    const LT = d3.map(links, linkTarget).map(intern);
    const G = d3.map(nodes, nodeGroup).map(intern);
    const nodeGroups = d3.sort(G);


    nodes = d3.map(nodes, (_, i) => ({ id: N[i], des: _.hasOwnProperty('des') ? _.des : "", isImportant: _.hasOwnProperty('important') ? true : false, sname: _.sname }));
    links = d3.map(links, (_, i) => ({ source: LS[i], target: LT[i], value: _.name, group: _.group }));

    const color = d3.scaleOrdinal(nodeGroups, colors);
    const forceNode = d3.forceManyBody().strength(-500);
    const forceLink = d3.forceLink(links).id(({ index: i }) => N[i]).distance(100);

    const simulation = d3.forceSimulation(nodes)
        .force("link", forceLink)
        .force("charge", forceNode)
        .force("center", d3.forceCenter())
        .on("tick", ticked);


    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

    svg.append("defs")
        .selectAll("marker")
        .data([1, 2])
        .enter()
        .append("marker")
        .attr("id", item => `arrow_${item}`)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", -0.5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("fill", item => {
            if (item == 1)
                return "rgba(0,240,0,0.7)"
            else return "rgba(240,0,0,0.7)"
        })
        .attr("d", "M0,-5L10,0L0,5");


    const link = svg.append("g")
        .attr('id', 'link')
        .attr("fill", "none")
        .attr("stroke-width", 1.5)
        .selectAll("path")
        .data(links)
        .join("path")
        .attr('id', (item, index) => `link_${item.index}`)
        .attr("stroke", item => {
            if (item.group == 1)
                return "rgb(31,119,180)"
            else return "rgb(255,127,14)"
        })
        .attr("marker-end", item => `url(#arrow_${item.group})`);

    svg.append("g")
        .attr('id', 'link_text')
        .selectAll('.pathText')
        .data(links)
        .enter()
        .append("text")
        .attr('fill', '#FFF')
        .attr("class", "pathText")
        .append('textPath')
        .attr("text-anchor", "middle")//居中
        .attr("startOffset", "50%")
        .attr('xlink:href', (item, index) => `#link_${item.index}`)
        .text(item => item.value);

    const defs = svg.append("defs").attr("id", "image_defs");

    const node = svg.append("g")
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", item => {
            if (item.isImportant)
                return nodeRadius * 1.4
            else return nodeRadius
        })
        .style("fill", item => {
            let ri = nodeRadius * 2
            if (item.isImportant)
                ri = nodeRadius * 2.8
            let catpattern = defs.append("pattern")
                .attr("id", `catpattern_${item.id}`)
                .attr("height", 1)
                .attr("width", 1);
            catpattern.append("image")
                .attr("x", 0)
                .attr("y", 0)
                .attr("id", `image_${item.id}`)
                .attr("width", ri)
                .attr("height", ri)
                .attr("xlink:href", `https://code.zwt666.top/img/rmdmy/${item.sname}.jpg`);
            return `url(#catpattern_${item.id})`
        })
        .attr("stroke-opacity", nodeStrokeOpacity)
        .attr("stroke-width", nodeStrokeWidth)
        .on("mouseover", (index, item) => {
            let ri = nodeRadius * 2 * 1.4
            if (item.isImportant)
                ri = nodeRadius * 2.8 * 1.4
            d3.select(index.target)
                .transition()
                .duration(200)
                .attr("r", () => {
                    if (item.isImportant)
                        return nodeRadius * 1.4 * 1.4
                    else return nodeRadius * 1.4
                })
            d3.select(`#image_${item.id}`)
                .transition()
                .duration(200)
                .attr("width", ri)
                .attr("height", ri)
            $('#force_des').text(item.des)
            $('#force_name').text(item.id)
            $('#force_message').css({ display: 'block' })
        })
        .on("mouseout", (index, item) => {
            let ri = nodeRadius * 2
            if (item.isImportant)
                ri = nodeRadius * 2.8
            d3.select(index.target)
                .transition()
                .duration(200)
                .attr("r", () => {
                    if (item.isImportant)
                        return nodeRadius * 1.4
                    else return nodeRadius
                })
            d3.select(`#image_${item.id}`)
                .transition()
                .duration(200)
                .attr("width", ri)
                .attr("height", ri)
            $('#force_message').css({ display: 'none' })
        })
        .on('mousemove', (ev) => {
            // console.log(ev)
            $('#force_message').css({ left: ev.clientX + 5 + 'px', top: (ev.clientY - 40.5) + 'px' })
        })
        .call(drag(simulation));

    svg.append("defs").append('pattern')
        .attr('id', "image")
        .attr('patternUnits', 'userSpaceOnUse')
        .attr('width', "100%")
        .attr('height', "100%")
        .attr("x", -500)
        .attr("y", -270)
        .append('image')
        .attr("xlink:href", "/src/assets/images/rmdmy.jpg")
        .attr("width", 1000)
        .attr("height", 540)
        .attr("x", 0)
        .attr("y", 0);

    if (G) node.attr("stroke", ({ index: i }) => color(G[i]))



    return Object.assign(svg.node(), { scales: { color } });
}

export default ForceGraph