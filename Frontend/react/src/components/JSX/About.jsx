import React from "react";
import "../CSS/About.css"
import Abdeslam from '../../assets/Group 9.png';
import Abdelhamid from '../../assets/Group 10.png';
import Profile from "../../assets/profile.png";
import Email from "../../assets/email_about.png";
import Phone from "../../assets/phone_about.png";
import Github from "../../assets/github_about.png";
import Linkedin from "../../assets/linkedin_about.png";
import Facebook from "../../assets/facebook_about.png";
import ab1 from "../../assets/aboutus_assets/ab1.png";
import ab2 from "../../assets/aboutus_assets/ab2.png";
import ab3 from "../../assets/aboutus_assets/ab3.png";
import ab4 from "../../assets/aboutus_assets/ab4.png";
import ab5 from "../../assets/aboutus_assets/ab5.png";
import ab6 from "../../assets/aboutus_assets/ab6.png";
import ab7 from "../../assets/aboutus_assets/ab7.png";
import ab8 from "../../assets/aboutus_assets/ab8.png";
import ab9 from "../../assets/aboutus_assets/ab9.png";
import ab10 from "../../assets/aboutus_assets/ab10.png";



export default function About() {
  return (
    <div className="column_About">
      <div className="row-view_About">
        <span className="text_About" >
          {"About Us"}
        </span>
        <img
          src={Profile}
          className="image_About"
        />
      </div>
      <div className="row-view2_About">
        <div className="view_About">
          <div className="column2_About">
            <div className="row-view3_About">
              <img
                src={Abdeslam}
                className="image2_About"
              />
              <div className="column3_About">
                <span className="text2_About" >
                  {"GOUNAICH Abdeslam"}
                </span>
                <div className="row-view4_About">
                  <img
                    src={Email}
                    className="image3_About"
                  />
                  <span className="text3_About" >
                    {"abdeslamgounaich@gmail.com"}
                  </span>
                </div>
                <div className="row-view5_About">
                  <img
                    src={Phone}
                    className="image4_About"
                  />
                  <span className="text4_About" >
                    {"0641559580"}
                  </span>
                </div>
              </div>
            </div>

            <div className="row-view6_About">
              <a href="https://www.facebook.com/abdeslam.gounaich/" target="_blank" rel="noopener noreferrer">
                <img
                  src={Facebook}
                  className="image5_About"
                  alt="Image 1"
                />
              </a>

              <a href="https://www.linkedin.com/in/abdeslam-gounaich-757998279/" target="_blank" rel="noopener noreferrer">
                <img
                  src={Linkedin}
                  className="image5_About"
                  alt="Image 2"
                />
              </a>

              <a href="https://github.com/GOUNAICH/" target="_blank" rel="noopener noreferrer">
                <img
                  src={Github}
                  className="image6_About"
                  alt="Image 3"
                />
              </a>
            </div>

          </div>
        </div>
        <div className="view2_About">
          <div className="column4_About">
            <div className="row-view3_About">
              <img
                src={Abdelhamid}
                className="image2_About"
              />
              <div className="column3_About">
                <span className="text5_About" >
                  {"Ben Drif Abdelhamid"}
                </span>
                <div className="row-view4_About">
                  <img
                    src={Email}
                    className="image3_About"
                  />
                  <span className="text3_About" >
                    {"abdelhamidbendrif@gmail.com"}
                  </span>
                </div>
                <div className="row-view5_About">
                  <img
                    src={Phone}
                    className="image4_About"
                  />
                  <span className="text4_About" >
                    {"0641559580"}
                  </span>
                </div>
              </div>
            </div>

            <div className="row-view6_About">
              <a href="https://www.facebook.com/profile.php?id=100011211101727" target="_blank" rel="noopener noreferrer">
                <img
                  src={Facebook}
                  className="image5_About"
                  alt="Image 4"
                />
              </a>

              <a href="https://www.linkedin.com/in/abdelhamid-ben-drif-10883928b/" target="_blank" rel="noopener noreferrer">
                <img
                  src={Linkedin}
                  className="image5_About"
                  alt="Image 5"
                />
              </a>

              <a href="https://github.com/abdelhamidbendrif" target="_blank" rel="noopener noreferrer">
                <img
                  src={Github}
                  className="image6_About"
                  alt="Image 6"
                />
              </a>
            </div>

          </div>
        </div>
      </div>


      <div className="column_Features">
        <span className="text_Features" >
          {"Features of Assistant"}
        </span>
        <div className="row-view_Features">
          <div className="view_Features">
            <div className="column2_Features">
              <div className="row-view2_Features">
                <img
                  src={ab1}
                  className="image_Features"
                />
                <span className="text2_Features" >
                  {"Face Recognition"}
                </span>
              </div>
              <div className="row-view3_Features">
                <img
                  src={ab2}
                  className="image2_Features"
                />
                <span className="text3_Features" >
                  {"Document scanning"}
                </span>
              </div>
              <div className="row-view4_Features">
                <img
                  src={ab3}
                  className="image3_Features"
                />
                <span className="text4_Features" >
                  {"Phone screen control"}
                </span>
              </div>

              {/* This is a comment inside JSX */}
              <div className="row-view12_Featurs">
                <img
                  src={ab4}
                  className="image12_Featurs"
                />
                <span className="text12_Featurs" >
                  {"Image generation and analysis"}
                </span>
              </div>
              <div className="row-view312_Featurs">
                <img
                  src={ab5}
                  className="image212_Featurs"
                />
                <span className="text312_Featurs" >
                  {"AI conversation"}
                </span>
              </div>

              {/* This is a comment inside JSX */}


            </div>
          </div>
          <div className="view_Features">
            <div className="column3_Features">
              <div className="row-view5_Features">
                <img
                  src={ab6}
                  className="image4_Features"
                />
                <span className="text5_Features" >
                  {"Email handling"}
                </span>
              </div>
              <div className="row-view6_Features">
                <img
                  src={ab7}
                  className="image5_Features"
                />
                <span className="text6_Features" >
                  {"Weather updates"}
                </span>
              </div>
              <div className="row-view7_Features">
                <img
                  src={ab8}
                  className="image6_Features"
                />
                <span className="text7_Features" >
                  {"Voice-controlled text editing"}
                </span>
              </div>
              {/* This is a comment inside JSX */}
              <div className="row-view412_Featurs">
                <img
                  src={ab9}
                  className="image312_Featurs"
                />
                <span className="text412_Featurs" >
                  {"PDF reading"}
                </span>
              </div>
              <div className="row-view512_Featurs">
                <img
                  src={ab10}
                  className="image412_Featurs"
                />
                <span className="text512_Featurs" >
                  {"App launching and web search"}
                </span>
              </div>
              {/* This is a comment inside JSX */}
            </div>
          </div>
        </div>
      </div>

    </div>
  )
}