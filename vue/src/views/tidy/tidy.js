import * as d3 from 'd3'
function Tidy(
  data,
  {
    path,
    id = Array.isArray(data) ? d => d.id : null,
    parentId = Array.isArray(data) ? d => d.parentId : null,
    children,
    tree = d3.tree,
    separation = tree === d3.tree ? (a, b) => (a.parent == b.parent ? 1 : 2) / a.depth : (a, b) => (a.parent == b.parent ? 1 : 2),
    sort,
    label,
    title,
    link,
    linkTarget = '_blank',
    width = 640,
    height = 400,
    margin = 60,
    marginTop = margin,
    marginRight = margin,
    marginBottom = margin,
    marginLeft = margin,
    radius = Math.min(width - marginLeft - marginRight, height - marginTop - marginBottom) / 2,
    r = 12,
    fill = '#888',
    stroke = '#BBB',
    strokeWidth = 2.5,
    strokeOpacity = 0.7,
    strokeLinejoin,
    strokeLinecap,
    halo = '#fff',
    haloWidth = 3
  }
) {
  const root = path != null ? d3.stratify().path(path)(data) : id != null || parentId != null ? d3.stratify().id(id).parentId(parentId)(data) : d3.hierarchy(data, children)

  if (sort != null) root.sort(sort)

  const descendants = root.descendants()
  const L = label == null ? null : descendants.map(d => label(d.data, d))

  const over2 = (par, now) => {
    d3.select(`#_${par.data.id}_${now.data.id}_`).attr('stroke', '#444')
    let parent = par.parent
    if (parent) over2(parent, par)
  }
  const over = (item, index) => {
    d3.select(item.target).attr('fill', '#444')
    let parent = index.parent
    if (parent) over2(parent, index)
  }

  const out = (item, index) => {
    d3.select(item.target).attr('fill', fill)
    d3.selectAll('path').attr('stroke', stroke)
  }

  tree()
    .size([2 * Math.PI, radius])
    .separation(separation)(root)

  const svg = d3
    .create('svg')
    .attr('viewBox', [-marginLeft - radius, -marginTop - radius, width, height])
    .attr('width', width)
    .attr('height', height)
    .attr('style', 'max-width: 100%; height: auto; height: intrinsic;')
    .attr('font-family', 'sans-serif')
    .attr('font-size', 10)

  svg
    .append('g')
    .attr('fill', 'none')
    .attr('stroke', stroke)
    .attr('stroke-opacity', strokeOpacity)
    .attr('stroke-linecap', strokeLinecap)
    .attr('stroke-linejoin', strokeLinejoin)
    .attr('stroke-width', strokeWidth)
    .selectAll('path')
    .data(root.links())
    .join('path')
    .attr('id', i => `_${i.source.data.id}_${i.target.data.id}_`)
    .attr(
      'd',
      d3
        .linkRadial()
        .angle(d => d.x)
        .radius(d => d.y)
    )

  const node = svg
    .append('g')
    .selectAll('a')
    .data(root.descendants())
    .join('a')
    .attr('xlink:href', link == null ? null : d => link(d.data, d))
    .attr('target', link == null ? null : linkTarget)
    .attr('transform', d => `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0)`)

  node
    .append('circle')
    .attr('fill', d => fill)
    .attr('r', r)
    .on('mouseover', over)
    .on('mouseout', out)

  if (title != null) node.append('title').text(d => title(d.data, d))

  if (L)
    node
      .append('text')
      .attr('transform', d => `rotate(${d.x >= Math.PI ? 180 : 0})`)
      .attr('dy', '0.32em')
      .attr('x', d => (d.x < Math.PI === !d.children ? 6 : -6))
      .attr('text-anchor', d => (d.x < Math.PI === !d.children ? 'start' : 'end'))
      .attr('paint-order', 'stroke')
      .attr('stroke', halo)
      .attr('stroke-width', haloWidth)
      .text((d, i) => L[i])

  return svg.node()
}

export default Tidy
