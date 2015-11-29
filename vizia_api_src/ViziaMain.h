#ifndef __VIZIA_MAIN_H__
#define __VIZIA_MAIN_H__

#include "ViziaDefines.h"
#include "ViziaDoomController.h"

#include <string>
#include <vector>


unsigned int DoomTics2Ms (unsigned int tics);
unsigned int Ms2DoomTics (unsigned int ms);

class ViziaMain{

    public:

        struct State{
            int number;
            std::vector<int> vars;
            int imageWidth;
            int imageHeight;
            int imagePitch;
            uint8_t* imageBuffer;
        };
        struct StateFormat{
            /* shape[0] - num. of channels, 1 - x, 2 - y */
            int imageShape[3];
            int varLen;
            StateFormat(){}
            StateFormat(int channels, int x, int y, int varLen)
            {
                this->imageShape[0] = channels;
                this->imageShape[1] = x;
                this->imageShape[2] = y;
                this->varLen = varLen;
            }
        };
        ViziaMain();
        virtual ~ViziaMain();

        bool loadConfig(std::string file);
        bool saveConfig(std::string file);

        int init();
        void close();

        void newEpisode();
        float makeAction(std::vector<bool>& actions);

        ViziaMain::State getState();
        std::vector<bool> getlastAction();
        bool isNewEpisode();
        bool isEpisodeFinished();

        void addAvailableButton(ViziaButton button);
        //void addAvailableButton(std::string action);

        void addStateAvailableVar(ViziaGameVar var);
        //void addStateAvailableVar(std::string var);

        //OPTIONS

        const ViziaDoomController* getController();

        void setDoomGamePath(std::string path);
        void setDoomIwadPath(std::string path);
        void setDoomFilePath(std::string path);
        void setDoomMap(std::string map);
        void setDoomSkill(int skill);
        void setDoomConfigPath(std::string path);

        void setAutoNewEpisode(bool set);
        void setNewEpisodeOnTimeout(bool set);
        void setNewEpisodeOnPlayerDeath(bool set);
        void setEpisodeTimeoutInMiliseconds(unsigned int ms);
        void setEpisodeTimeoutInDoomTics(unsigned int tics);

        void setScreenResolution(unsigned int width, unsigned int height);
        void setScreenWidth(unsigned int width);
        void setScreenHeight(unsigned int height);
        void setScreenFormat(ViziaScreenFormat format);
        void setRenderHud(bool hud);
        void setRenderWeapon(bool weapon);
        void setRenderCrosshair(bool crosshair);
        void setRenderDecals(bool decals);
        void setRenderParticles(bool particles);

        StateFormat getStateFormat();
        int getActionFormat();
        int getScreenWidth();
        int getScreenHeight();
        size_t getScreenPitch();
        size_t getScreenSize();
        ViziaScreenFormat getScreenFormat();

    private:

        ViziaDoomController * doomController;

        std::vector<ViziaGameVar> stateAvailableVars;
        std::vector<ViziaButton> availableButtons;

        std::vector<bool> lastAction;

        bool initialized;

        StateFormat stateFormat;
        State state;

};

#endif