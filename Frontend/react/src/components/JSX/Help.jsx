import React, { useState } from "react";
import vedio from '../../assets/assistant_vedio.mp4';

import "../CSS/Help.css"
export default function Helpt() {

  return (
    <div className="column_content_Help ">
      <div className="profile_container_Help ">
        <img
          src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/tlstigkr_expires_30_days.png"
          className="profile_image_Help "
        />
      </div>


      <div className="column_Help">
        <span className="text_Help" >
          {"Video Tutorials"}
        </span>
        <div className="row-view_Help">
          <button className="button_Help">
            <div className="column2_Help">
              <div className="row-view2_Help">
                <img
                  src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/aleqjd4w_expires_30_days.png"}
                  className="image_Help"
                />
                <span className="text2_Help" >
                  {"How to Use Voice Commands"}
                </span>
              </div>
              <div className="row-view3_Help">
                <img
                  src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/cqzcfwdm_expires_30_days.png"}
                  className="image2_Help"
                />
                <span className="text3_Help" >
                  {"How to Generate Images"}
                </span>
              </div>
              <div className="row-view4_Help">
                <img
                  src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/n0qhif7k_expires_30_days.png"}
                  className="image3_Help"
                />
                <span className="text4_Help" >
                  {"Phone screen control"}
                </span>
              </div>
              <div className="row-view5_Help">
                <img
                  src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/5v71qchs_expires_30_days.png"}
                  className="image4_Help"
                />
                <span className="text5_Help" >
                  {"How to Send Emails . . ."}
                </span>
              </div>
              <div className="row-view6_Help">
                <img
                  src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/n0wqrxco_expires_30_days.png"}
                  className="image5_Help"
                />
                <span className="text6_Help" >
                  {"Watch these short videos to learn how to use key features"}
                </span>
              </div>
            </div>
          </button>
          <video
            src={vedio}
            className="image6_Help"
            /* autoPlay*/
            muted
            loop
            playsInline
            controls
          />
        </div>
      </div>



      <div className="Command_List_div">
        <div className="column_Help_List2">
          <span className="text_Help2">{"Command List"}</span>
        </div>
        <div className="view_Help_List">
          <div className="row-view_Help_List">
            <div className="column_Help_List">
              <span className="text_Help_List">• how are you</span>
              <span className="text_Help_List">• who built you</span>
              <span className="text_Help_List">• help me</span>
              <span className="text_Help_List">• who made you</span>
            </div>
            <div className="column2_Help_List">
              <span className="text_Help_List">• open notepad</span>
              <span className="text_Help_List">• open (any app name)</span>
              <span className="text_Help_List">• search for (something)</span>
              <span className="text_Help_List">• send email</span>
            </div>
            <div className="column3_Help_List">
              <span className="text_Help_List">• what time is it</span>
              <span className="text_Help_List">• display my phone</span>
              <span className="text_Help_List">• generate image for</span>
              <span className="text_Help_List">• describe image...</span>
            </div>
            <div className="view2_Help_List">
              <div className="box_Help_List"></div>
            </div>
          </div>
        </div>
      </div>


    </div>
  )
}