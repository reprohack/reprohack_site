## Event HackMD Introductory slides template

This template can be used for slides written and hosted on HackMD during a ReproHack event. <https://hackmd.io/>

If you are new to HackMD, please see this [short guide](https://hackmd.io/@turingway/hackmd-guide) by the Turing Way or the [full HackMD Tutorial Book](https://hackmd.io/c/tutorials/%2Fs%2Ftutorials) and in particular, the chapter on [Making Presentation Slides with HackMD](https://hackmd.io/c/tutorials/%2Fs%2Fhow-to-create-slide-deck)


The most important setting to note is that to you view the sldes you need to **enable** <i class="fa fa-tv"></i> **Slide Mode** in the top right sharing <i class="fa fa-share-alt fa-18"></i> menu and hit "**Preview**" to see your slide.

![](https://i.imgur.com/Ov8F3IV.png =450x)


### Template

##### _Copy and paste into new HackMD document_

<br>

    ---
    title: <your-event-name> ReproHack slides
    tags: ReproHack, introduction, slides
    description: View the slide with "Slide Mode".
    slideOptions:
        theme: white
    ---

    ## Welcome to the <your-event-name> ReproHack!

    <!-- Put the link to this slide here so people can follow -->
    <br>

    ### Event Page: 
    ### http://reprohack.org/event/<your-event-id>/

    Contains all event information and links to materials

    ---
    <!-- Add any housekeeping details here. If running an online event, you might want to include an introduction to the platform here --> 

    ### House Keeping:

    - No Fire Alarm test today
    - Toilets & Fire Exit
    - Water point - downstairs



    ---

    # Introductions

    <!-- Use this section as an ice-breaker. Introduce yourself, then allow others to 
    go around the room and introduce themselves too. If online, consider using break-out rooms of 5-6 people -->

    ---

    <!-- Add details about yourself the organiser here: -->

    ## Who am I?

    ### Dr Anna Krystalli (@annakrystalli)

    - Research Software Engineer _University of Sheffield_
    - 2019 Fellow _Software Sustainability Institute_
    - Software Peer Review Editor _rOpenSci_ 
    - Co-organiser _Sheffield R Users Group_

    ---

    ## Why am I here?

    I believe there's lots to learn about Reproducibility from working with real published projects.

    ---

    ## Who is my favorite animated character?

    Stitch!

    ![](https://media3.giphy.com/media/95MU6SEzeLnUc/giphy.gif?cid=790b76115d11033236595055776d483b&rid=giphy.gif)

    ---

    <!-- Open it up to participants -->

    ## Who are you?

    ## Why are you here?

    ## Who is your favorite animated character?


    ---

    # Welcome Back

    ## Introduction & tips for reviewing

    ---

    ## ReproHack Objectives

    1. **Practical Experience in Reproducibility**

    3. **Feedback to Authors**

    5. **Think more broadly about opportunities and challenges**

    ---

    # Plan of Action

    ---

    ### Reproduce paper

    1. **Project review and team formation**


    2. **Select and register your project**

    3. **Work on your project!**

    4. **Re-group part-way through.**

    6. **Feedback at the end (group & authors)**

    ---

    <!-- Remind participant of code of conduct and basic expectations. Bring attention to the additional considerations involved in giving feedback to authors -->
    ## Code of Conduct

    Event governed by [**ReproHack Code of Conduct**](https://reprohack.org/code-of-conduct)

    <br>

    ### Additional Considerations

    - #### Reproducibility is hard!
    - #### Submitting authors are incredibly brave!



    ---

    ## Thank you Authors! :raised_hands: 

    - #### Without them there would be no ReproHack.
    - #### Show gratitude and appreciation for their effort and bravery. :pray: 
    - #### Constructive criticism only please!


    ---

    # Reproduce and Review

    # :mag:

    ---

    ## Selecting Papers

    - **No. attempts:** No. times reproduction has been attempted
    - **Mean Repro Score:** Mean reproducibility score (out of 10)
        - lower == harder!


    ---

    ## Review as an auditor :bookmark_tabs:

    ---


    ## Access

    - How easy was it to gain access to the materials?

    ## Installation

    - How easy / automated was installation?
    - Did you have any problems?

    ---

    ## Data
    - Were data clearly separated from code and other items?
    - Were large data files deposited in a trustworthy data repository and referred to using a persistent identifier?
    - Were data documented ...somehow...

    ---


    ## Documentation

    Was there adequate documentation describing:
    - how to install necessary software including non-standard dependencies?
    - how to use materials to reproduce the paper?
    - how to cite the materials, ideally in a form that can be copy and pasted?

    ---

    ## Analysis

    - Were you able to fully reproduce the paper? :white_check_mark:
    - How automated was the process of reproducing the paper?
    - How easy was it to link analysis code to:
    - the plots it generates
    - sections in the manuscript in which it is described

    ---

    ## Analysis

    ### If the analysis was not fully reproducible :no_entry_sign:
    - Did results (e.g. model outputs, tables, figures) differ to those published? By how much?
    - Were missing dependencies?
    - Was the computational environment not adequately described / captured?

    ---

    ## Review as a user :video_game:

    <br>

    #### What did you find easy / intuitive?



    #### What did you find confusing / difficult



    #### What did you enjoy?

    ---

    # Feed back

    # :speech_balloon: 

    ---


    ## Feedback as a community member

    <br>

    #### Acknowledge author effort

    #### Give feedback in good faith

    #### Focus on community benefits and system level solutions

    ---

    # Additional activities

    ---

    ## Finished early?


    ### Explore the work more deeply:
    - Try and run additional analyses.
    - Create new plots. 
    - Combine materials with your own or other open materials available on the web!


    ---

    # Resources

    - [**Example Compendium**](https://github.com/annakrystalli/rrcompendiumDTB): Demo Research compendium 
    - [**The Turing Way**](https://the-turing-way.netlify.com/introduction/introduction): a lightly opinionated guide to reproducible data science.
    - [**Statistical Analyses and Reproducible Research**](): Gentleman and Temple Lang's introduction of the concept of Research Compendia
    - [**Packaging data analytical work reproducibly using R (and friends)**](https://peerj.com/preprints/3192/): how researchers can improve the reproducibility of their work using research compendia based on R packages and related tools



    ---

    # Let's go! :checkered_flag: 

    ---

    ## 1. Paper review

    + Have a look at the papers available for reproduction


    ## 2. Team formation / project registration

    + Fine to work individually
    + Add your details to the [**hackpad**](https://hackmd.io/6nhNpD0VTHaCLuXPBy-dFw?both#Leeds).
    + Register your team and paper on the [**hackpad**](https://hackmd.io/6nhNpD0VTHaCLuXPBy-dFw?both#Leeds)

    ---

    ## 3. Mid-point regroup

    - Which paper have you selected? Briefly describe what it's about.
    - Briefly describe the approach to reproducibility the paper has taken.
    - Anything in particular you like about the paper's approach so far?
    - Anything you're having difficulty with?

    ---

    ## 4. Feedback to authors

    - **Please complete the feedback form for authors**
    - Feel free to record general findings the hackpad

    ---

    ## 5. Final regroup

    - So, how did you get on? 
    - Final comments.
    - If there's time, tackle some discussion topics (see hackpad).
    - On post-its: One thing you liked, one thing that can be improved.

    ---



    # Get involved!


    ### Visit ReproHack Hub <https://reprohack.org>

    - [**Submit a paper for review**](https://reprohack.org/paper/new/)
    - [**Organise your own event**](https://reprohack.org/event/new/)

    _Check out our [Resources](https://reprohack.org/resources) for more details_

    ### Chat to us:

    [![Slack](https://img.shields.io/badge/slack-join%20us-orange?style=for-the-badge&logo=slack)](https://reprohack-autoinvite.herokuapp.com/)


    ---

    # THANK YOU ALL! :pray: 

    - ### Thank you PARTICIPANTS for coming!
    - ### Thank you AUTHORS for submitting!
    - ### Thank to <any-sponsors> for sponsoring!


    # :wave: 

