-- Pandoc's docx writer silently drops inline `style="color: ..."` on Spans
-- (unlike its HTML/ODT writers). Map such spans/divs to a named Word
-- character style instead (defined in reference.docx), which the docx
-- writer does honor via `custom-style`. This is what keeps \aiflag{...}
-- (AI suggestions) red and \begin{esboco} gray/italic in the exported
-- DOCX, per the marking convention in specs/constitution.md.
local function style_for(color)
  if color and color:match('red') then return 'AIFlagRed' end
  if color and color:match('gray') then return 'EsbocoGray' end
  return nil
end

local function map_color_to_style(el)
  local style = el.attributes['style']
  if style then
    local color = style:match('color:%s*([%a]+)')
    local mapped = style_for(color)
    if mapped then
      el.attributes['custom-style'] = mapped
      el.attributes['style'] = nil
    end
  end
  return el
end

Span = map_color_to_style
Div = map_color_to_style
