import re, sys, os
X=os.environ["STAGE"]
p=X+"/Includes_Parameters.xml"
s=open(p,encoding="utf-8").read()

# --- locate old include
i=s.index('<include name="ParamWidgetInclude">')
k=s.rindex('<include>$PARAM[content]</include>')+len('<include>$PARAM[content]</include>')
k=s.index('</control>',k)+len('</control>')       # closes the old page list
j=s.index('</include>',k)+len('</include>')       # closes ParamWidgetInclude
old=s[i:j]
# the visibility condition of the old page container, reused unchanged
m=re.search(r'<control id="\$PARAM\[ID\]" type="fixedlist">.*?<visible>(.*?)</visible>', old, re.S)
page_visible=m.group(1)
# content lines of the 8 hidden lists (keep target/sort/list), raise limit
contents={}
for n in range(1,9):
    mm=re.search(r'<control id="\$PARAM\[ID\]%d" type="list">.*?(<content [^>]*>.*?</content>)'%n, old, re.S)
    c=mm.group(1).replace('limit="6"','limit="40"')
    contents[n]=c


def V(m): return "Integer.IsGreater(Container($PARAM[ID]%d).NumItems,0)" % m
def navs(n):
    out=[]
    # down: first visible row after n
    for m in range(n+1,9):
        cond=" + ".join([V(m)]+["!"+V(k) for k in range(n+1,m)])
        out.append('<ondown condition="%s">SetFocus($PARAM[ID]0%d)</ondown>'%(cond,m))
    out.append('<ondown>noop</ondown>')
    # up: first visible row before n
    for m in range(n-1,0,-1):
        cond=" + ".join([V(m)]+["!"+V(k) for k in range(m+1,n)])
        out.append('<onup condition="%s">SetFocus($PARAM[ID]0%d)</onup>'%(cond,m))
    out.append('<onup>noop</onup>')
    return "\n\t\t\t\t\t".join(out)

GM='String.IsEqual(Skin.String($PARAM[ID]0-WidgetList-1),plugin://plugin.program.htpc.games/)'

def row(n, gm=None):
    c=contents[n]
    return f'''
			<control type="group">
				<visible>!String.IsEmpty(Skin.String($PARAM[ID]0-WidgetList-{n})) + Integer.IsGreater(Container($PARAM[ID]{n}).NumItems,0){(' + '+gm) if gm else ''}</visible>
				<height>860</height>
				<control type="label">
					<left>16</left>
					<top>6</top>
					<width>2800</width>
					<height>80</height>
					<font>Med34</font>
					<aligny>center</aligny>
					<textcolor>ffbcbcbc</textcolor>
					<label>$INFO[Skin.String($PARAM[ID]0-WidgetLabel-{n})]</label>
					<visible>!Control.HasFocus($PARAM[ID]0{n})</visible>
				</control>
				<control type="label">
					<left>16</left>
					<top>6</top>
					<width>2800</width>
					<height>80</height>
					<font>Med34</font>
					<aligny>center</aligny>
					<textcolor>ffffffff</textcolor>
					<label>$INFO[Skin.String($PARAM[ID]0-WidgetLabel-{n})]</label>
					<visible>Control.HasFocus($PARAM[ID]0{n})</visible>
				</control>
				<control type="label">
					<left>1900</left>
					<top>6</top>
					<width>1000</width>
					<height>80</height>
					<font>Light26</font>
					<align>right</align>
					<aligny>center</aligny>
					<textcolor>ff7a7c80</textcolor>
					<label>Press X for options</label>
					<visible>Control.HasFocus($PARAM[ID]0{n})</visible>
				</control>
				<control id="$PARAM[ID]0{n}" type="fixedlist">
					<left>0</left>
					<top>90</top>
					<width>2940</width>
					<height>770</height>
					<orientation>horizontal</orientation>
					<viewtype label="">list</viewtype>
					<focusposition>0</focusposition>
					<preloaditems>2</preloaditems>
					<scrolltime easing="inout" tween="sine">250</scrolltime>
					<onleft>ClearProperty(HubFanart,Home)</onleft>
					<onleft>99</onleft>
					<onback>ClearProperty(HubFanart,Home)</onback>
					<onback>99</onback>
					<onright>noop</onright>
					{navs(n)}
					<onclick condition="String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,episode)">Action(Info)</onclick>
					<onclick condition="ListItem.IsFolder + !String.IsEqual(ListItem.DBType,movie) + !String.IsEqual(ListItem.DBType,episode)">ActivateWindow(Videos,$INFO[ListItem.FolderPath],return)</onclick>
					<onclick condition="!ListItem.IsFolder + !String.IsEqual(ListItem.DBType,movie) + !String.IsEqual(ListItem.DBType,episode)">PlayMedia($INFO[ListItem.FileNameAndPath])</onclick>
					<itemlayout height="770" width="460">
						<control type="group">
							<left>40</left>
							<top>20</top>
							<control type="image">
								<width>380</width>
								<height>570</height>
								<aspectratio align="center">scale</aspectratio>
								<texture background="true" colordiffuse="d0ffffff" fallback="views/movie_fallback.png">$VAR[PosterImage]</texture>
							</control>
								<control type="textbox">
									<left>24</left>
									<top>190</top>
									<width>332</width>
									<height>200</height>
									<font>Med28</font>
									<aligny>center</aligny>
									<align>center</align>
									<textcolor>ffbcbcbc</textcolor>
									<label>$INFO[ListItem.Label]</label>
									<visible>String.IsEmpty(ListItem.Art(poster)) + String.IsEmpty(ListItem.Art(tvshow.poster)) + String.IsEmpty(ListItem.Art(thumb))</visible>
								</control>
							<control type="image">
								<width>110</width>
								<height>110</height>
								<texture>$INFO[ListItem.VideoResolution,views/resolution/,.png]</texture>
							</control>
							<control type="image">
								<width>110</width>
								<height>110</height>
								<texture>views/OverlayWatched.png</texture>
								<visible>String.IsEqual(ListItem.Overlay,OverlayWatched.png) + [!Integer.IsEqual(ListItem.Property(NumEpisodes),0) | String.IsEmpty(ListItem.Property(NumEpisodes))]</visible>
							</control>
							<control type="label">
								<top>588</top>
								<width>380</width>
								<height>56</height>
								<font>Light22</font>
								<textcolor>ffd8d8d8</textcolor>
								<label>$VAR[GridTitleLabel]</label>
							</control>
							<control type="label">
								<top>648</top>
								<width>380</width>
								<height>48</height>
								<font>Light22</font>
								<textcolor>ff7a7c80</textcolor>
								<label>$VAR[GridSubLabel]</label>
							</control>
						</control>
					</itemlayout>
					<focusedlayout height="770" width="460">
						<control type="button">
							<include>HiddenControl</include>
							<onfocus>SetProperty(HubFanart,$INFO[ListItem.Art(fanart)],Home)</onfocus>
						</control>
						<control type="group">
							<left>40</left>
							<top>20</top>
							<control type="group">
							<animation center="190,285" easing="inout" effect="zoom" end="105" start="100" time="200" tween="sine">Focus</animation>
							<control type="image">
								<left>-8</left>
								<top>-8</top>
								<width>396</width>
								<height>586</height>
								<texture colordiffuse="ffe9a01e">common/white_square.png</texture>
								<visible>Control.HasFocus($PARAM[ID]0{n})</visible>
							</control>
							<control type="image">
								<width>380</width>
								<height>570</height>
								<aspectratio align="center">scale</aspectratio>
								<texture background="true" fallback="views/movie_fallback.png">$VAR[PosterImage]</texture>
							</control>
								<control type="textbox">
									<left>24</left>
									<top>190</top>
									<width>332</width>
									<height>200</height>
									<font>Med28</font>
									<aligny>center</aligny>
									<align>center</align>
									<textcolor>ffbcbcbc</textcolor>
									<label>$INFO[ListItem.Label]</label>
									<visible>String.IsEmpty(ListItem.Art(poster)) + String.IsEmpty(ListItem.Art(tvshow.poster)) + String.IsEmpty(ListItem.Art(thumb))</visible>
								</control>
							<control type="image">
								<width>110</width>
								<height>110</height>
								<texture>$INFO[ListItem.VideoResolution,views/resolution/,.png]</texture>
							</control>
							<control type="image">
								<width>110</width>
								<height>110</height>
								<texture>views/OverlayWatched.png</texture>
								<visible>String.IsEqual(ListItem.Overlay,OverlayWatched.png) + [!Integer.IsEqual(ListItem.Property(NumEpisodes),0) | String.IsEmpty(ListItem.Property(NumEpisodes))]</visible>
							</control>
							</control>
							<control type="label">
								<top>588</top>
								<width>380</width>
								<height>56</height>
								<font>Light22</font>
<scroll>false</scroll>
								<textcolor>ffe9a01e</textcolor>
								<label>$VAR[GridTitleLabel]</label>
								<visible>Control.HasFocus($PARAM[ID]0{n})</visible>
							</control>
							<control type="label">
								<top>588</top>
								<width>380</width>
								<height>56</height>
								<font>Light22</font>
<scroll>false</scroll>
								<textcolor>ffd8d8d8</textcolor>
								<label>$INFO[ListItem.Label]</label>
								<visible>!Control.HasFocus($PARAM[ID]0{n})</visible>
							</control>
							<control type="label">
								<top>648</top>
								<width>380</width>
								<height>48</height>
								<font>Light22</font>
<scroll>false</scroll>
								<textcolor>ffa4a4a4</textcolor>
								<label>$VAR[GridSubLabel]</label>
							</control>
						</control>
					</focusedlayout>
					{c}
				</control>
			</control>'''

def gridrow(n):
    """Same row, but a wrapped multi-row grid (used for the Games page)."""
    r=row(n, GM)
    r=r.replace("<height>860</height>","<height>1860</height>",1)
    r=r.replace("$PARAM[ID]0%d"%n,"$PARAM[ID]9%d"%n)
    r=r.replace('type="fixedlist"','type="panel"',1)
    r=r.replace("<orientation>horizontal</orientation>","<orientation>vertical</orientation>",1)
    r=r.replace("<height>770</height>","<height>1760</height>",1)
    r=r.replace("<focusposition>0</focusposition>","",1)
    r=r.replace('limit="40"','limit="100"')
    return r

def rows():
    out=""
    for n in range(1,9):
        if n==1:
            out+=row(1,"!"+GM)+gridrow(1)
        else:
            out+=row(n)
    return out

hidden=""
for n in range(1,9):
    c1=contents[n].replace('limit="40"','limit="1"')
    hidden+=f'''
		<control id="$PARAM[ID]{n}" type="list">
			<include>HiddenList</include>
			{c1}
		</control>'''
# keep tiny hidden lists with the OLD ids so other code (counts) is unaffected? the visible rows own ids ID1..ID8 now.
new = '''<include name="ParamWidgetInclude">''' + hidden + '''
		<control id="$PARAM[ID]" type="grouplist">
			<left>900</left>
			<top>300</top>
			<width>2940</width>
			<height>1860</height>
			<orientation>vertical</orientation>
			<itemgap>0</itemgap>
			<scrolltime easing="inout" tween="sine">250</scrolltime>
			<onleft>ClearProperty(HubFanart,Home)</onleft>
			<onleft>99</onleft>
			<onback>ClearProperty(HubFanart,Home)</onback>
			<onback>99</onback>
			<include>WindowHomeFadeAnimation</include>
			<visible>''' + page_visible + '''</visible>''' + rows() + '''
		</control>
	</include>'''
s=s[:i]+new+s[j:]
open(p,"w",encoding="utf-8").write(s)
print("page visible:", page_visible[:120])
print("rows generated; new include length", len(new))
