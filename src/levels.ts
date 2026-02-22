export interface LevelParams {
    name: string;
    objective: string;
    map: string;
    par: number;
}

export const levels: LevelParams[] = [
    {
        name: "The Basics",
        objective: "Use h, j, k, l to navigate your cursor '@' to the Exit 'E'.",
        par: 14,
        map: `
###########
#    #    #
# C  #  E #
#    #    #
#         #
###########
`
    },
    {
        name: "The Snake Maze",
        objective: "Navigate the winding path using h, j, k, l efficiently.",
        par: 70,
        map: `
#####################
#C                  #
################### #
#                   #
# ###################
#                   #
################### #
#E                  #
#####################
`
    },
    {
        name: "Word Jumping",
        objective: "Use w (next start), e (next end), and b (prev start) to jump across the words rapidly!",
        par: 22,
        map: `
######################################
#C                                   #
#  apple   banana   cherry   date    #
#                                    #
#  elephant   fig   grape   honey    #
#                                    #
#  igloo   jungle   kite   lemon     #
#                                    #
#  mango   nest     owl    peach     #
#                                   E#
######################################
`
    }
];
