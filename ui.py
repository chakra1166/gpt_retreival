import streamlit as st
import base64


# def header_ui(title="Yinson Annual Report Chat Demo"):
#     st.markdown(
#         """
#         <style>
#         .pageheader {
#             padding: 0px;
#             width: 100%;
#             margin-left: 0px;
#             margin-top: -60px;
#             margin-bottom: 50px;
#         }
#         .pagetitle {
#             text-align: center;
#             #position: absolute;
#             width: 100%;
#             margin-bottom: 10px;
#             border: 2px #FFEA0D;
#             font-size: 30px;
#             font-weight: bold;
#             padding: 10px;
#             border-radius: 10px;
#             background-color: #2E247D;
#             #color: black;
#             color: #FFEA0D;
#         }
#         .logo-img {
#         float:left;
#     }
#     """,
#         unsafe_allow_html=True,
#     )

#     metric_style = f"""
#     <style>
#     div.css-1r6slb0.e1tzin5v2 {{
#         border: 1.5px solid black;
#         padding: 5px;
#         text-align: center;
#         border-radius: 10px;
#         margin-bottom: 20px;
#         background-color: #F9F9F9;
#         }}
#     div.row-widget.stButton {{
#         text-align: center;
#     }}
#     button.css-629wbf.edgvbvh10 {{
#         border: 1px solid black;
#         background-color: #004B93;
#         color: white;
#         margin: auto;
#     }}
#     <style>
#     """
#     st.markdown(metric_style, unsafe_allow_html=True)

#     st.markdown(
#         f"""
#         <div class='pageheader'>
#             <p class='pagetitle'>
#                 {title}
#             </p>
#         </div>""",
#         unsafe_allow_html=True,
#     )


def header_ui():
    image_name = "logo"
    title = "Sustainability Report Chat Demo"
    img = f"{image_name}.png"

    st.markdown(
        f"""<h5 style='text-align: center; width:100%; font-size: 20px; padding: 20px; border-radius: 5px; color: #1A191F; background-color:rgba(231,130,4,1); margin-left: 10px;'>
                        <center><b>{title}</b></center>
                    </h5>""",
        unsafe_allow_html=True,
    )

    # st.markdown(
    #     f"""
    #     <div style="margin-top: -73px; margin-left: -800px">
    #             <center><img  src="data:image/png;base64,{base64.b64encode(open(img, "rb").read()).decode()}", width = "180" height = "80"></center>
    #     </div>""",
    #     unsafe_allow_html=True,
    # )
